# # app/domains/tenants/models/tenant_user_role.py
# from __future__ import annotations
# from typing import Optional
# from uuid import UUID
# from sqlmodel import Field, SQLModel, Relationship
# from sqlalchemy.orm import Mapped
# from app.db.base_class import APIBase

# class TenantUserRole(APIBase, table=True):
#     __tablename__ = "tenant_user_roles"

#     tenant_user_id: UUID = Field(foreign_key="public.tenant_users.id", primary_key=True)
#     tenant_role_id: UUID = Field(foreign_key="public.tenant_roles.id", primary_key=True)

#     tenant_user: Mapped[Optional["TenantUser"]] = Relationship(
#         back_populates="user_roles",
#         sa_relationship_kwargs={
#             "primaryjoin": "TenantUserRole.tenant_user_id == foreign(TenantUser.id)",
#             "foreign_keys": "[TenantUserRole.tenant_user_id]"
#         }
#     )
#     tenant_role: Mapped[Optional["TenantRole"]] = Relationship(
#         back_populates="user_roles",
#         sa_relationship_kwargs={
#             "primaryjoin": "TenantUserRole.tenant_role_id == foreign(TenantRole.id)",
#             "foreign_keys": "[TenantUserRole.tenant_role_id]"
#         }
#     )

#     assigned_at: Optional[str] = Field(default=None)
#     assigned_by: Optional[UUID] = Field(default=None, foreign_key="public.users.id")
