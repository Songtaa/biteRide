# app/domains/auth/models/role.py
from __future__ import annotations
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import APIBase

class Role(APIBase):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=False)

    user_roles: Mapped[List["UserRole"]] = relationship(back_populates="role")
    role_permissions: Mapped[List["RolePermission"]] = relationship(back_populates="role")
