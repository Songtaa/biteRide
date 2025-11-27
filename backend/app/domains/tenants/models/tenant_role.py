# app/domains/tenants/models/tenant_role.py
from __future__ import annotations
from typing import List
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from app.db.base_class import APIBase


class TenantRole(APIBase):
    __tablename__ = "tenant_roles"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.tenants.id")
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="tenant_schema_roles")

    user_roles: Mapped[List["TenantUserRole"]] = relationship(back_populates="role")
    role_permissions: Mapped[List["TenantRolePermission"]] = relationship(back_populates="role")

    users: Mapped[List["TenantUser"]] = relationship(
        secondary="tenant_user_roles",
        back_populates="roles",
        viewonly=True
    )
