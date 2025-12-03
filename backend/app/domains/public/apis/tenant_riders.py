# app/api/routes/tenant_riders.py
from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_master_session, get_tenant_session # master for public repos, get_tenant_session for tenant context
from app.domains.public.repository.rider_tenant import RiderTenantRepository
from app.domains.public.repository.rider import RiderRepository
from app.domains.public.repository.tenant import TenantRepository
from app.domains.public.services.rider_tenant import RiderTenantService
from app.domains.public.schemas.rider_tenant import RiderTenantRead

tenant_rider_router = APIRouter(prefix="/tenants/{tenant_id}/riders", tags=["Tenant Riders"], responses={404: {"description": "Not found"}})


async def get_master_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_master_session() as session:
        yield session


def get_rider_tenant_service(session: AsyncSession = Depends(get_master_session_dep)):
    return RiderTenantService(
        rider_tenant_repo=RiderTenantRepository(session),
        rider_repo=RiderRepository(session),
        tenant_repo=TenantRepository(session),
    )


ServiceDep = Annotated[RiderTenantService, Depends(get_rider_tenant_service)]


@tenant_rider_router.post("/{rider_id}", response_model=RiderTenantRead, operation_id="AssignRiderToTenant")
async def assign_rider(tenant_id: UUID, rider_id: UUID, service: ServiceDep):
    mapping = await service.assign_rider_to_tenant(tenant_id, rider_id)
    return mapping


@tenant_rider_router.delete("/{rider_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="RemoveRiderFromTenant")
async def remove_rider(tenant_id: UUID, rider_id: UUID, service: ServiceDep):
    await service.remove_rider_from_tenant(tenant_id, rider_id)
    return None


@tenant_rider_router.get("/", response_model=list[RiderTenantRead], operation_id="ListTenantRiders")
async def list_riders_for_tenant(tenant_id: UUID, service: ServiceDep):
    return await service.list_riders_for_tenant(tenant_id)
