from typing import Optional
from uuid import UUID

from sqlmodel import Field
from sqlmodel import Field, Relationship


from app.db.base_class import APIBase


class UserTenant(APIBase, table=True):
    __tablename__ = "user_tenants"
    __table_args__ = {"schema": "public"}

    user_id: int = Field(foreign_key="public.users.id", primary_key=True)

    tenant_id: int = Field(foreign_key="public.tenants.id", primary_key=True)
    is_admin: bool = Field(default=False)
    school_id: Optional[UUID] = Field(default=None, foreign_key="schools.id")

    tenant_roles: List["TenantRole"] = Relationship(
        back_populates="users",
        link_model=TenantUserRole
    )
    
    tenant_user_permissions: List["TenantUserPermission"] = Relationship(
        back_populates="user"
    )