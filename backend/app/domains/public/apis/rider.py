# app/api/routes/riders.py

from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.domains.tenants.repository import RiderRepository
from app.domains.tenants.services.rider import RiderService
from app.domains.tenants.schemas import (
    RiderCreate,
    RiderUpdate,
    RiderOut
)

router = APIRouter(prefix="/riders", tags=["Riders"])


def get_rider_service(session: AsyncSession = Depends(get_session)):
    repo = RiderRepository(session)
    return RiderService(repo)


@router.post("/", response_model=RiderOut)
async def create_rider(
    data: RiderCreate,
    service: RiderService = Depends(get_rider_service)
):
    return await service.create_rider(data)


@router.get("/{rider_id}", response_model=RiderOut)
async def get_rider(
    rider_id: UUID,
    service: RiderService = Depends(get_rider_service)
):
    return await service.get_rider(rider_id)


@router.put("/{rider_id}", response_model=RiderOut)
async def update_rider(
    rider_id: UUID,
    data: RiderUpdate,
    service: RiderService = Depends(get_rider_service)
):
    return await service.update_rider(rider_id, data)


@router.delete("/{rider_id}", status_code=204)
async def delete_rider(
    rider_id: UUID,
    service: RiderService = Depends(get_rider_service)
):
    await service.delete_rider(rider_id)
    return None


@router.get("/", response_model=list[RiderOut])
async def search_riders(
    field: str,
    value: str,
    service: RiderService = Depends(get_rider_service),
):
    return await service.search_riders(field, value)


@router.patch("/{rider_id}/status", response_model=RiderOut)
async def update_rider_status(
    rider_id: UUID,
    status: str,
    service: RiderService = Depends(get_rider_service)
):
    return await service.update_status(rider_id, status)
