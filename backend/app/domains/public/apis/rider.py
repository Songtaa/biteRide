# app/api/routes/riders.py

from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import db_session_dependency, get_master_session

from app.domains.public.repository.rider import RiderRepository
from app.domains.public.services.rider import RiderService
from app.domains.public.schemas.rider import (
    RiderCreate,
    RiderUpdate,
    RiderOut
)
from app.utils.auth_dep import AccessTokenBearer

rider_router = APIRouter(prefix="/riders", tags=["Riders"], responses={404: {"description": "Not found"}})

async def get_master_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_master_session() as session:
        yield session

sessionDep = Annotated[AsyncSession, Depends(get_master_session_dep)]
    
access_token_bearer = Annotated[dict, Depends(AccessTokenBearer())]



@rider_router.post("/rider", response_model=RiderOut, status_code=status.HTTP_201_CREATED)
async def create_rider(
    data: RiderCreate,
    service: RiderService = Depends(sessionDep)
):
    return await service.create_rider(data)


@rider_router.get("/{rider_id}", response_model=RiderOut)
async def get_rider(
    rider_id: UUID,
    service: RiderService = Depends(sessionDep)
):
    return await service.get_rider(rider_id)


@rider_router.put("/{rider_id}", response_model=RiderOut)
async def update_rider(
    rider_id: UUID,
    data: RiderUpdate,
    service: RiderService = Depends(sessionDep)
):
    return await service.update_rider(rider_id, data)


@rider_router.delete("/{rider_id}", status_code=204)
async def delete_rider(
    rider_id: UUID,
    service: RiderService = Depends(sessionDep)
):
    await service.delete_rider(rider_id)
    return None


@rider_router.get("/", response_model=list[RiderOut])
async def search_riders(
    field: str,
    value: str,
    service: RiderService = Depends(sessionDep),
):
    return await service.search_riders(field, value)


@rider_router.patch("/{rider_id}/status", response_model=RiderOut)
async def update_rider_status(
    rider_id: UUID,
    status: str,
    service: RiderService = Depends(sessionDep)
):
    return await service.update_status(rider_id, status)
