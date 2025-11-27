# # app/domains/tenants/models/tenant_user_permission.py
# from __future__ import annotations
# from typing import Optional
# from uuid import UUID
# from sqlmodel import Field, SQLModel, Relationship
# from sqlalchemy.orm import Mapped
# from app.db.base_class import APIBase

# class TenantUserPermission(APIBase, table=True):
#     __tablename__ = "tenant_user_permissions"

#     tenant_user_id: UUID = Field(foreign_key="public.tenant_users.id", primary_key=True)
#     tenant_permission_id: UUID = Field(foreign_key="public.tenant_permissions.id", primary_key=True)

#     tenant_user: Mapped[Optional["TenantUser"]] = Relationship(back_populates="user_permissions")
#     tenant_permission: Mapped[Optional["TenantPermission"]] = Relationship(back_populates="user_permissions")

#     expires_at: Optional[str] = Field(default=None)
#     scope: Optional[str] = Field(default=None)
# #