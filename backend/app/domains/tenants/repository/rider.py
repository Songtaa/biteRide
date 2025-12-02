from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseRepository
from app.domains.tenants.models import Rider
from app.domains.tenants.schemas import RiderCreate, RiderUpdate


class RiderRepository(BaseRepository[Rider, RiderCreate, RiderUpdate]):

    def __init__(self, session: AsyncSession):
        super().__init__(Rider, session)

    async def get_by_phone(self, phone: str) -> Optional[Rider]:
        stmt = select(Rider).where(Rider.phone == phone)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[Rider]:
        stmt = select(Rider).where(Rider.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_available(self) -> List[Rider]:
        stmt = select(Rider).where(Rider.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()
