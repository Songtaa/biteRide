from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from pydantic import EmailStr

from app.db.base_class import APIBase

if TYPE_CHECKING:
    from app.domains.auth.models.rbac_models import Permission


# ---------------------------------------------------------------------------
# Link Models
# ---------------------------------------------------------------------------

class TenantUserRole(APIBase, table=True):
    __tablename__ = "tenant_user_roles"

    user_id: UUID = Field(foreign_key="tenant_users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="tenant_roles.id", primary_key=True)
    tenant_id: UUID = Field(foreign_key="public.tenants.id", primary_key=True)

    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[UUID] = Field(default=None, foreign_key="tenant_users.id")


class TenantRolePermission(APIBase, table=True):
    __tablename__ = "tenant_role_permissions"

    role_id: UUID = Field(foreign_key="tenant_roles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="public.permissions.id", primary_key=True)

    granted_at: datetime = Field(default_factory=datetime.utcnow)
    granted_by: Optional[UUID] = Field(default=None, foreign_key="tenant_users.id")


class TenantUserPermission(APIBase, table=True):
    __tablename__ = "tenant_user_permissions"

    user_id: UUID = Field(foreign_key="tenant_users.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="public.permissions.id", primary_key=True)
    expires_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Core Tenant Models
# ---------------------------------------------------------------------------

class TenantUser(APIBase, table=True):
    __tablename__ = "tenant_users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: Optional[str] = Field(default=None, max_length=255)
    tenant_id: UUID = Field(foreign_key="public.tenants.id", nullable=False)

    tenant_roles: List["TenantRole"] = Relationship(
        back_populates="users",
        link_model=TenantUserRole,
    )

    tenant_user_permissions: List[TenantUserPermission] = Relationship(
        back_populates="user"
    )


class TenantRole(APIBase, table=True):
    __tablename__ = "tenant_roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, index=True)
    description: Optional[str] = Field(default=None, max_length=200)
    is_system: bool = Field(default=False)
    tenant_id: UUID = Field(foreign_key="public.tenants.id", nullable=False)

    users: List[TenantUser] = Relationship(
        back_populates="tenant_roles",
        link_model=TenantUserRole,
    )

    permissions: List["Permission"] = Relationship(
        back_populates="tenant_roles",
        link_model=TenantRolePermission,
    )

    role_permissions: List[TenantRolePermission] = Relationship(
        back_populates="role"
    )


# ---------------- Configure Cross-Relationships ----------------

TenantRolePermission.role = Relationship(back_populates="role_permissions")
TenantRolePermission.permission = Relationship(back_populates="tenant_roles")

TenantUserPermission.user = Relationship(back_populates="tenant_user_permissions")
TenantUserPermission.permission = Relationship(back_populates="tenant_user_permissions")
