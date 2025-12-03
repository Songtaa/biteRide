# app/services/rider_service.py
from typing import List
from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.public.repository.rider import RiderRepository
from app.domains.public.schemas.rider import RiderCreate, RiderUpdate, RiderRead


class RiderService:
    def __init__(self, repo: RiderRepository):
        self.repo = repo

    async def create_rider(self, session: AsyncSession, data: RiderCreate):
        # ensure unique phone
        if await self.repo.get_by_phone(data.phone):
            raise HTTPException(status_code=400, detail="Phone already exists")
        return await self.repo.create(data)

    async def get_rider(self, session: AsyncSession, rider_id: UUID):
        rider = await self.repo.get_by_id(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return rider

    async def update_rider(self, session: AsyncSession, rider_id: UUID, data: RiderUpdate):
        rider = await self.repo.get_by_id(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return await self.repo.update(db_obj=rider, obj_in=data)

    async def delete_rider(self, session: AsyncSession, rider_id: UUID) -> bool:
        rider = await self.repo.get_by_id(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return await self.repo.delete(rider_id)

    async def list_riders(self, session: AsyncSession):
        # reuse BaseRepository.search or get_all
        return await self.repo.get_all()
