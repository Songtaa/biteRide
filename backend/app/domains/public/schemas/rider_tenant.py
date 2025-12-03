# app/schemas/rider_tenant.py
from uuid import UUID
from sqlmodel import SQLModel



class RiderTenantBase(SQLModel):
    tenant_id: UUID
    rider_id: UUID

    model_config = {"from_attributes": True}


class RiderTenantCreate(RiderTenantBase):
    pass


class RiderTenantRead(RiderTenantBase):
    model_config = {"from_attributes": True}
