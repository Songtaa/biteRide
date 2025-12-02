from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException

from app.repositories.rider_repository import RiderRepository
from app.schemas.rider import (
    RiderCreate,
    RiderUpdate,
    RiderOut,
)


class RiderService:
    def __init__(self, rider_repo: RiderRepository):
        self.rider_repo = rider_repo

    async def create_rider(self, data: RiderCreate) -> RiderOut:
        return await self.rider_repo.create(data)

    async def get_rider(self, rider_id: UUID) -> RiderOut:
        rider = await self.rider_repo.get_by_id(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return rider

    async def update_rider(self, rider_id: UUID, data: RiderUpdate) -> RiderOut:
        rider = await self.get_rider(rider_id)
        return await self.rider_repo.update(db_obj=rider, obj_in=data)

    async def delete_rider(self, rider_id: UUID) -> bool:
        exists = await self.rider_repo.get_by_id(rider_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Rider not found")

        return await self.rider_repo.delete(rider_id)

    async def search_riders(self, field: str, value: str) -> List[RiderOut]:
        return await self.rider_repo.search(field=field, value=value)

    async def update_status(self, rider_id: UUID, status: str) -> RiderOut:
        rider = await self.get_rider(rider_id)
        return await self.rider_repo.update(db_obj=rider, obj_in={"status": status})
