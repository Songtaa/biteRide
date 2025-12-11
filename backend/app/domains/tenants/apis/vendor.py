## app/domains/tenants/apis/vendor.py

from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.tenant_dependencies import get_tenant_id_from_context
from app.db.session import get_tenant_session
from app.domains.tenants.schemas.vendor import (
    VendorCreate,
    VendorUpdate,
    VendorRead,
)
from app.domains.tenants.repository.vendor import VendorRepository
from app.domains.tenants.services.vendor import VendorService


vendor_router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"],
    responses={404: {"description": "Vendor not found"}},
)


async def session_dep() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_tenant_session():
        yield session


def vendor_service_dep(
    session: AsyncSession = Depends(session_dep),
) -> VendorService:
    repo = VendorRepository(session)
    return VendorService(repo)


ServiceDep = Annotated[VendorService, Depends(vendor_service_dep)]
TenantID = Annotated[UUID, Depends(get_tenant_id_from_context)]



@vendor_router.post(
    "",
    response_model=VendorRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_vendor(
    tenant_id: TenantID,
    data: VendorCreate,
    service: ServiceDep,
):
    return await service.create_vendor(tenant_id, data)


@vendor_router.get(
    "/{vendor_id}",
    response_model=VendorRead,
)
async def get_vendor(
    vendor_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.get_vendor(vendor_id, tenant_id)



@vendor_router.put(
    "/{vendor_id}",
    response_model=VendorRead,
)
async def update_vendor(
    vendor_id: UUID,
    tenant_id: TenantID,
    data: VendorUpdate,
    service: ServiceDep,
):
    return await service.update_vendor(vendor_id, tenant_id, data)



@vendor_router.delete(
    "/{vendor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_vendor(
    vendor_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    await service.soft_delete_vendor(vendor_id, tenant_id)
    return None


@vendor_router.delete(
    "/{vendor_id}/hard-delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def hard_delete_vendor(
    vendor_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    await service.hard_delete_vendor(vendor_id, tenant_id)
    return None
