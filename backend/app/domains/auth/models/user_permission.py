# app/domains/auth/models/user_permission.py
from __future__ import annotations
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class UserPermission(APIBase):
    __tablename__ = "user_permissions"
    __table_args__ = {"schema": "public"}

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.users.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.permissions.id"), primary_key=True)

    expires_at: Mapped[Optional[str]] = mapped_column(default=None)
    scope: Mapped[Optional[str]] = mapped_column(default=None)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="user_permissions")
