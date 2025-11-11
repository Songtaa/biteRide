from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from pydantic import EmailStr
from app.db.base_class import APIBase

# Runtime imports for link models (must be real classes)
# from app.domains.school.models.tenant_user_role import TenantUserRole
from app.domains.school.models.tenant_user_permission import TenantUserPermission

if TYPE_CHECKING:
    from app.domains.school.models.tenant_role import TenantRole
    from app.domains.school.models.school import School


class TenantUser(APIBase, table=True):
    __tablename__ = "tenant_users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: Optional[str] = Field(default=None, max_length=255)

    tenant_id: UUID = Field(foreign_key="public.tenants.id")
    school_id: Optional[UUID] = Field(default=None, foreign_key="schools.id")

    # Relationships
    school: Optional["School"] = Relationship()

    tenant_roles: list["TenantRole"] = Relationship(
        back_populates="users",
        link_model=TenantUserRole
    )
    tenant_user_permissions: list["TenantUserPermission"] = Relationship(
        back_populates="user"
    )
    # tenant_user_roles: list["TenantUserRole"] = Relationship(
    #     back_populates="user"
    # )
