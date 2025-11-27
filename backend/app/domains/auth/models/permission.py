# app/domains/auth/models/permission.py
from __future__ import annotations
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import APIBase

class Permission(APIBase):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "public"}

    name: Mapped[str] = mapped_column(unique=True, index=True)
    resource: Mapped[str] = mapped_column(nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(default="")

    role_permissions: Mapped[List["RolePermission"]] = relationship(back_populates="permission")
    user_permissions: Mapped[List["UserPermission"]] = relationship(back_populates="permission")
