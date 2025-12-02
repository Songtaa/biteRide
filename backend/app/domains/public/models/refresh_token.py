# app/domains/auth/models/refresh_token.py
from __future__ import annotations
from typing import Optional
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class RefreshToken(APIBase):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "public"}

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.users.id"), primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=False)
    expiration_time: Mapped[Optional[datetime]] = mapped_column(default=None)

    user: Mapped[Optional["User"]] = relationship(back_populates="refresh_tokens", viewonly=True)
