# app/domains/tenants/models/tenant_permission.py
from __future__ import annotations
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import APIBase


    


class TenantPermission(APIBase):
    __tablename__ = "tenant_permissions"
    __table_args__ = {"schema": "public"}


    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    resource: Mapped[str] = mapped_column(index=True)
    action: Mapped[str] = mapped_column(index=True)
    is_global: Mapped[bool] = mapped_column(default=False)

    role_permissions: Mapped[List["TenantRolePermission"]] = relationship(back_populates="tenant_permission")
    user_permissions: Mapped[List["TenantUserPermission"]] = relationship(back_populates="tenant_permission")
