from uuid import UUID
from sqlmodel import SQLModel


class AssignRiderToTenant(SQLModel):
    rider_id: UUID


class TenantRiderLinkRead(SQLModel):
    rider_id: UUID
    tenant_id: UUID
