# from __future__ import annotations
# from typing import List, Optional, TYPE_CHECKING
# from uuid import UUID, uuid4

# from sqlmodel import Field, Relationship
# from sqlalchemy import Column, String

# from app.db.base_class import APIBase

# if TYPE_CHECKING:
#     from app.domains.auth.models.refresh_token import RefreshToken
#     from app.domains.auth.models.token_blocklist import TokenBlocklist
#     from app.domains.tenants.models.tenant_rbac_models import (
#         TenantRole,
#         TenantUserPermission,
#         TenantRolePermission,
#     )
#     from app.domains.auth.models.rbac_models import User, Permission

# # -----------------------------------
# # Link Models
# # -----------------------------------

# class UserRole(APIBase, table=True):
#     __tablename__ = "user_roles"
#     __table_args__ = {"schema": "public"}

#     user_id: UUID = Field(foreign_key="public.users.id", primary_key=True)
#     role_id: UUID = Field(foreign_key="public.roles.id", primary_key=True)
#     tenant_id: Optional[UUID] = Field(foreign_key="public.tenants.id", default=None)


# class RolePermission(APIBase, table=True):
#     __tablename__ = "role_permissions"
#     __table_args__ = {"schema": "public"}

#     role_id: UUID = Field(foreign_key="public.roles.id", primary_key=True)
#     permission_id: UUID = Field(foreign_key="public.permissions.id", primary_key=True)


# class UserPermission(APIBase, table=True):
#     __tablename__ = "user_permissions"
#     __table_args__ = {"schema": "public"}

#     user_id: UUID = Field(foreign_key="public.users.id", primary_key=True)
#     permission_id: UUID = Field(foreign_key="public.permissions.id", primary_key=True)

#     user = Relationship(
#         sa_relationship_kwargs={
#             "primaryjoin": "UserPermission.user_id == User.id",
#             "back_populates": "user_permissions",
#             "foreign_keys": "[UserPermission.user_id]"
#         }
#     )
#     permission = Relationship(
#         sa_relationship_kwargs={
#             "primaryjoin": "UserPermission.permission_id == Permission.id", 
#             "back_populates": "user_permissions",
#             "foreign_keys": "[UserPermission.permission_id]"
#         }
#     )
    
# # -----------------------------------
# # Core Models
# # -----------------------------------

# class User(APIBase, table=True):
#     __tablename__ = "users"
#     __table_args__ = {"schema": "public"}

#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     email: str = Field(
#         sa_column=Column(String(255), nullable=False, unique=True)
#     )
#     password: str = Field(nullable=False, max_length=255)
#     is_active: bool = Field(default=True)
#     is_superuser: bool = Field(default=False)
#     full_name: Optional[str] = Field(default=None, max_length=255)

#     roles: List["Role"] = Relationship(
#         back_populates="users",
#         link_model=UserRole,
#     )

#     user_permissions: List["UserPermission"] = Relationship(
#         back_populates="user"
#     )

#     tokens: List["TokenBlocklist"] = Relationship(
#         back_populates="global_user",
#         sa_relationship_kwargs={"viewonly": True},
#     )

#     refresh_token: Optional["RefreshToken"] = Relationship(
#         back_populates="user",
#         sa_relationship_kwargs={"uselist": False, "viewonly": True},
#     )


# class Role(APIBase, table=True):
#     __tablename__ = "roles"
#     __table_args__ = {"schema": "public"}

#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     name: str = Field(index=True, unique=True, max_length=50)
#     description: Optional[str] = Field(default=None, max_length=500)

#     users: List["User"] = Relationship(
#         back_populates="roles",
#         link_model=UserRole,
#     )

#     permissions: List["Permission"] = Relationship(
#         back_populates="roles",
#         link_model=RolePermission,
#     )


# class Permission(APIBase, table=True):
#     __tablename__ = "permissions"
#     __table_args__ = {"schema": "public"}

#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     name: str = Field(index=True)
#     description: Optional[str] = Field(default=None, max_length=500)

#     roles: List["Role"] = Relationship(
#         back_populates="permissions",
#         link_model=RolePermission,
#     )

#     user_permissions: List["UserPermission"] = Relationship(
#         back_populates="permission"
#     )

#     # tenant view relationships
#     tenant_roles: List["TenantRole"] = Relationship(
#         back_populates="permissions",
#         sa_relationship_kwargs={"viewonly": True},
#     )

#     tenant_user_permissions: List["TenantUserPermission"] = Relationship(
#         back_populates="permission",
#         sa_relationship_kwargs={"viewonly": True},
#     )

#     tenant_role_permissions: List["TenantRolePermission"] = Relationship(
#         back_populates="permission",
#         sa_relationship_kwargs={"viewonly": True},
#     )