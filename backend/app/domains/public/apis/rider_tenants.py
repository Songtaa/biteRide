# app/api/routes/rider_tenants.py
from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, Depends
from uuid import UUID

from app.db.session import get_master_session
from app.domains.public.repository.rider_tenant import RiderTenantRepository
from app.domains.public.repository.rider import RiderRepository
from app.domains.public.repository.tenant import TenantRepository
from app.domains.public.services.rider_tenant import RiderTenantService

rider_tenant_router = APIRouter(prefix="/riders/{rider_id}/tenants", tags=["Rider Tenants"])


async def get_master_session_dep():
    async with get_master_session() as session:
        yield session


def get_rider_tenant_service(session = Depends(get_master_session_dep)):
    return RiderTenantService(
        rider_tenant_repo=RiderTenantRepository(session),
        rider_repo=RiderRepository(session),
        tenant_repo=TenantRepository(session),
    )


ServiceDep = Annotated[RiderTenantService, Depends(get_rider_tenant_service)]


@rider_tenant_router.get("/", operation_id="ListTenantsForRider")
async def list_tenants_for_rider(rider_id: UUID, service: ServiceDep):
    return await service.list_tenants_for_rider(rider_id)
