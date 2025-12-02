# app/domains/auth/models/user.py
from __future__ import annotations
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base_class import APIBase

class User(APIBase):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    # username: Mapped[str] = mapped_column(index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    full_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_superuser: bool = False

    # Relationships
    user_roles: Mapped[List["UserRole"]] = relationship(back_populates="user")
    user_permissions: Mapped[List["UserPermission"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(back_populates="user")
    tokens: Mapped[List["TokenBlocklist"]] = relationship(back_populates="global_user")

    tenants: Mapped[list["UserTenant"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )