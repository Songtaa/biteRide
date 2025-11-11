from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from app.db.base_class import APIBase


class TenantRolePermission(APIBase, table=True):
    __tablename__ = "tenant_role_permissions"

    role_id: UUID = Field(
        foreign_key="tenant_roles.id",
        primary_key=True
    )
    permission_id: UUID = Field(
        foreign_key="public.permissions.id",
        primary_key=True
    )

    granted_at: Optional[datetime] = Field(default_factory=datetime.now)
    granted_by: Optional[UUID] = Field(default=None, foreign_key="tenant_users.id")
    # role: List["TenantRole"] = Relationship(back_populates="permissions")
