from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from app.db.base_class import APIBase

# Runtime imports for link models
from app.domains.school.models.tenant_role_permission import TenantRolePermission
from app.domains.school.models.tenant_user_role import TenantUserRole

if TYPE_CHECKING:
    from app.domains.auth.models.tenant_user import TenantUser
    from app.domains.school.models.tenant_permission import TenantPermission


class TenantRoleBase(APIBase):
    name: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=200)
    is_system: bool = Field(default=False)


class TenantRole(TenantRoleBase, table=True):
    __tablename__ = "tenant_roles"

    permissions: List["TenantPermission"] = Relationship(
        back_populates="roles",
        link_model=TenantRolePermission
    )
    users: List["TenantUser"] = Relationship(
        back_populates="roles",
        link_model=TenantUserRole
    )