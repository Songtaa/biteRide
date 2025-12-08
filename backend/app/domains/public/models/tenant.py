# app/domains/tenants/models/tenant.py

from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID

from app.db.base_class import APIBase


class Tenant(APIBase):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    schema_name: Mapped[str] = mapped_column(index=True, unique=True)
    subdomain: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    billing_tier: Mapped[str] = mapped_column(default="basic")

    tenant_schema_users: Mapped[list["TenantUser"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    tenant_schema_roles: Mapped[list["TenantRole"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    
    tenant_users: Mapped[list["UserTenant"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    riders: Mapped[list["Rider"]] = relationship(
        secondary="rider_tenant_link",
        back_populates="tenants",
        viewonly=True
    )

    payment_configs: Mapped[list["PaymentGatewayConfig"]] = relationship(
    back_populates="tenant",
    cascade="all, delete-orphan"
    )
