from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import APIBase


class Vendor(APIBase):
    __tablename__ = "vendors"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("public.tenants.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    opening_hours: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Soft delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tenant = relationship("Tenant", back_populates="vendors")
