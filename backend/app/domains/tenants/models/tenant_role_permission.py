# # app/domains/tenants/models/tenant_role_permission.py
# from __future__ import annotations
# from typing import Optional
# from uuid import UUID
# from sqlmodel import Field, SQLModel, Relationship
# from sqlalchemy.orm import Mapped
# from app.db.base_class import APIBase

# class TenantRolePermission(APIBase, table=True):
#     __tablename__ = "tenant_role_permissions"

#     tenant_role_id: UUID = Field(foreign_key="public.tenant_roles.id", primary_key=True)
#     tenant_permission_id: UUID = Field(foreign_key="public.tenant_permissions.id", primary_key=True)

#     tenant_role: Mapped[Optional["TenantRole"]] = Relationship(back_populates="role_permissions")
#     tenant_permission: Mapped[Optional["TenantPermission"]] = Relationship(back_populates="role_permissions")

#     granted_at: Optional[str] = Field(default=None)
