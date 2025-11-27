# app/domains/tenants/models/link_rbac_models.py
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

if TYPE_CHECKING:
    from app.domains.tenants.models.tenant_user import TenantUser
    from app.domains.tenants.models.tenant_role import TenantRole
    from app.domains.tenants.models.tenant_permission import TenantPermission


class TenantUserRole(APIBase):
    __tablename__ = "tenant_user_roles"

    tenant_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenant_users.id", ondelete="CASCADE"),
        primary_key=True
    )
    tenant_role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenant_roles.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relationships
    tenant_user: Mapped[Optional["TenantUser"]] = relationship(back_populates="user_roles")
    role: Mapped[Optional["TenantRole"]] = relationship(back_populates="user_roles")


class TenantRolePermission(APIBase):
    __tablename__ = "tenant_role_permissions"

    tenant_role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenant_roles.id", ondelete="CASCADE"),
        primary_key=True
    )
    tenant_permission_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.tenant_permissions.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relationships
    role: Mapped[Optional["TenantRole"]] = relationship(back_populates="role_permissions")
    tenant_permission: Mapped[Optional["TenantPermission"]] = relationship(back_populates="role_permissions")


class TenantUserPermission(APIBase):
    __tablename__ = "tenant_user_permissions"

    tenant_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenant_users.id", ondelete="CASCADE"),
        primary_key=True
    )
    tenant_permission_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.tenant_permissions.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relationships
    tenant_user: Mapped[Optional["TenantUser"]] = relationship(back_populates="user_permissions")
    tenant_permission: Mapped[Optional["TenantPermission"]] = relationship(back_populates="user_permissions")