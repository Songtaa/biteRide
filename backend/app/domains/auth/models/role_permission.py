# app/domains/auth/models/role_permission.py
from __future__ import annotations
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class RolePermission(APIBase):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "public"}

    role_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.roles.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.permissions.id"), primary_key=True)

    granted_at: Mapped[Optional[str]] = mapped_column(default=None)

    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")
