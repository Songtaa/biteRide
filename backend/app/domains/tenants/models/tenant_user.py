# app/domains/tenants/models/tenant_user.py
from __future__ import annotations
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from app.db.base_class import APIBase


class TenantUser(APIBase):
    __tablename__ = "tenant_users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    email: Mapped[str] = mapped_column(index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # belongs to the tenant's schema
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.tenants.id"),
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="tenant_schema_users")

    # RBAC
    user_roles: Mapped[List["TenantUserRole"]] = relationship(back_populates="tenant_user")
    user_permissions: Mapped[List["TenantUserPermission"]] = relationship(back_populates="tenant_user")

    roles: Mapped[List["TenantRole"]] = relationship(
        secondary="tenant_user_roles",
        back_populates="users",
        viewonly=True
    )
