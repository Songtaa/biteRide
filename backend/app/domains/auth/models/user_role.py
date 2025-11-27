# app/domains/auth/models/user_role.py
from __future__ import annotations
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class UserRole(APIBase):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": "public"}

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.users.id"), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.roles.id"), primary_key=True)
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.tenants.id"), nullable=True)

    assigned_at: Mapped[Optional[str]] = mapped_column(default=None)
    assigned_by: Mapped[Optional[int]] = mapped_column(default=None)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="user_roles")
