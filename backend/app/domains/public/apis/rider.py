from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_master_session

from app.domains.public.repository.rider import RiderRepository
from app.domains.public.services.rider import RiderService
from app.domains.public.schemas.rider import (
    RiderCreate,
    RiderUpdate,
    RiderOut
)


rider_router = APIRouter(
    prefix="/riders",
    tags=["Riders"],
    responses={404: {"description": "Not found"}},
)


async def get_master_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_master_session() as session:
        yield session


def get_rider_service(
    session: AsyncSession = Depends(get_master_session_dep),
):
    repo = RiderRepository(session)
    return RiderService(repo)

ServiceDep = Annotated[RiderService, Depends(get_rider_service)]


@rider_router.post(
    "/rider",
    response_model=RiderOut,
    status_code=status.HTTP_201_CREATED,
    operation_id="TenantCreateRider"
)
async def create_rider(
    data: RiderCreate,
    service: ServiceDep,
):
    return await service.create_rider(data)


@rider_router.get(
    "/{rider_id}",
    response_model=RiderOut,
    operation_id="TenantGetRider"
)
async def get_rider(
    rider_id: UUID,
    service: ServiceDep,
):
    return await service.get_rider(rider_id)


@rider_router.put(
    "/{rider_id}",
    response_model=RiderOut,
    operation_id="TenantUpdateRider"
)
async def update_rider(
    rider_id: UUID,
    data: RiderUpdate,
    service: ServiceDep,
):
    return await service.update_rider(rider_id, data)


@rider_router.delete(
    "/{rider_id}",
    status_code=204,
    operation_id="TenantDeleteRider"
)
async def delete_rider(
    rider_id: UUID,
    service: ServiceDep,
):
    await service.delete_rider(rider_id)
    return None


@rider_router.get(
    "/", 
    response_model=list[RiderOut],
    operation_id="TenantSearchRiders"
)
async def search_riders(
    field: str,
    value: str,
    service: ServiceDep,
):
    return await service.search_riders(field, value)


@rider_router.patch(
    "/{rider_id}/status",
    response_model=RiderOut,
    operation_id="TenantUpdateRiderStatus"
)
async def update_rider_status(
    rider_id: UUID,
    status: str,
    service: ServiceDep,
):
    return await service.update_status(rider_id, status)
