# app/domains/tenants/models/user_tenant.py

from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base_class import APIBase


class UserTenant(APIBase):
    __tablename__ = "user_tenants"
    __table_args__ = {"schema": "public"}

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.users.id"),
        primary_key=True,
    )

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.tenants.id"),
        primary_key=True,
    )

    is_admin: Mapped[bool] = mapped_column(default=False)

    # Only link global tables
    user: Mapped["User"] = relationship(back_populates="tenants")
    tenant: Mapped["Tenant"] = relationship(back_populates="tenant_users")
