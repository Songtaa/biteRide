from datetime import datetime
from uuid import UUID
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.db.base_class import APIBase

from sqlmodel import Field, Relationship, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped

class TenantUserRole(APIBase, table=True):
    __tablename__ = "tenant_user_roles"

    user_id: UUID = Field(foreign_key="tenant_users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="tenant_roles.id", primary_key=True)
    tenant_id: UUID = Field(
        foreign_key="public.tenants.id", nullable=False, primary_key=True
    )
    assigned_at: datetime = Field(default_factory=datetime.now)
    assigned_by: Optional[UUID] = Field(default=None, foreign_key="tenant_users.id")
    # user: Optional["TenantUser"] = Relationship(back_populates="tenant_user_roles")
    # role: Optional["TenantRole"] = Relationship(back_populates="user_assignments")


