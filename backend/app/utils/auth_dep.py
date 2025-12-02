from typing import Annotated, Any, List, Set

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.domains.public.repository.token_blocklist import TokenBlocklistRepository
# from app.domains.public.repository.token_blocklist import TokenRepository
from app.domains.public.services.token import TokenService
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import db_session_dependency
from app.domains.public.models.user import User
from app.db.redis import token_in_blocklist

# from src.db.redis import token_in_blocklist
from app.utils.dependencies import get_master_session_dep
from app.domains.public.services.user_service import UserService
from app.domains.public.repository.user_repository import UserRepository
from app.utils.security import Security
from app.utils.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    AccountNotVerified,
)
from app.domains.public.services.user_service import UserService
from app.domains.public.services.role import RoleService

# sessionDep = Annotated[AsyncSession, Depends(db_session_dependency)]
sessionDep = Annotated[AsyncSession, Depends(get_master_session_dep)]


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = Security.decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        
        token_repo = TokenBlocklistRepository(request.state.session)
        token_service = TokenService(token_repo)

        if not await token_service.verify_token_not_blocklisted(token_data["jti"]):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = Security.decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()


# async def get_current_user(
#     session: sessionDep,
#     token_data: dict = Depends(AccessTokenBearer()),
# ) -> User:
#     tenant = token_data.get("tenant")  # May be None for superusers
#     jti = token_data.get("jti")

#     blocklist_repo = TokenBlocklistRepository(session)
#     if await blocklist_repo.is_token_blocked(jti, tenant):
#         raise HTTPException(status_code=401, detail="Token has been revoked")

#     # Get email directly from token_data, not from token_data["user"]
#     user_email = token_data["email"]
#     user_service = UserService(session, User)
#     user = await user_service.repository.get_user_by_email(user_email)

#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user


# def SuperuserRequired(current_user: User = Depends(get_current_user)):
#     if not getattr(current_user, "is_superuser", False):
#         raise HTTPException(status_code=403, detail="Superuser access required")
#     return current_user


# class RoleChecker:
#     def __init__(self, allowed_roles: List[str]) -> None:
#         self.allowed_roles = allowed_roles

#     def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
#         # if not current_user.is_verified:
#         #     raise AccountNotVerified()
#         if current_user.roles in self.allowed_roles:
#             return True

#         raise InsufficientPermission()


async def get_current_user(
    session: sessionDep,
    token_data: dict = Depends(AccessTokenBearer()),
) -> User:
    tenant = token_data.get("tenant")  # May be None for superusers
    jti = token_data.get("jti")
    
    blocklist_repo = TokenBlocklistRepository(session)
    if await blocklist_repo.is_token_blocked(jti, tenant):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    
    user_email = token_data["email"]
    user_service = UserService(session)
    user = await user_service.repository.get_user_by_email(user_email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    role_service = RoleService(session)
    # Eager load roles and permissions
    user.roles = await role_service.get_roles_by_user(user.id)
    
    return user

def SuperuserRequired(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=403, detail="Superuser access required")
    return current_user

class PermissionChecker:
    def __init__(self, required_permissions: Set[str]):
        self.required_permissions = required_permissions
    
    async def __call__(
        self, 
        current_user: User = Depends(get_current_user),
        session: sessionDep = None
    ) -> bool:
        # Superusers have all permissions
        if getattr(current_user, "is_superuser", False):
            return True
        
        # Collect all permissions from user's roles
        user_permissions = set()
        for role in current_user.roles:
            for permission in role.permissions:
                user_permissions.add(permission.name)
        
        # Check if user has all required permissions
        if not self.required_permissions.issubset(user_permissions):
            raise HTTPException(
                status_code=403, 
                detail=f"Required permissions: {self.required_permissions}"
            )
        return True

class RoleChecker:
    def __init__(self, allowed_roles: Set[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(
        self, 
        current_user: User = Depends(get_current_user)
    ) -> bool:
        # Superusers can access any role-protected endpoint
        if getattr(current_user, "is_superuser", False):
            return True
        
        # Check if user has any of the required roles
        user_roles = {role.name for role in current_user.roles}
        print(f"First item type: {type(current_user.roles[0]) if current_user.roles else 'Empty'}")
        if not user_roles.intersection(self.allowed_roles):
            raise HTTPException(
                status_code=403, 
                detail=f"Required roles: {self.allowed_roles}"
            )
        return True

# Permission-based dependencies
can_read_users = PermissionChecker({"users:read"})
can_write_users = PermissionChecker({"users:write"})
can_delete_users = PermissionChecker({"users:delete"})

# Role-based dependencies
admin_required = RoleChecker({"admin"})
editor_required = RoleChecker({"editor"})




access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
