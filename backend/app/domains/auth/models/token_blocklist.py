# app/domains/auth/models/token_blocklist.py
from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class TokenBlocklist(APIBase):
    __tablename__ = "token_blocklist"
    __table_args__ = {"schema": "public"}

    jti: Mapped[str] = mapped_column(nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    global_user_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("public.users.id"), nullable=True)
    tenant_user_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    tenant: Mapped[Optional[str]] = mapped_column(default=None, index=True)

    global_user: Mapped[Optional["User"]] = relationship(back_populates="tokens", viewonly=True)
