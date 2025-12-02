from typing import List, Optional
from uuid import UUID
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.base import BaseRepository
from app.models.rider_tenant import RiderTenant
from app.schemas.rider import RiderTenantCreate


class RiderTenantRepository(BaseRepository[RiderTenant, RiderTenantCreate, dict]):

    def __init__(self, session: AsyncSession):
        super().__init__(RiderTenant, session)


    async def get_mapping(self, tenant_id: UUID, rider_id: UUID) -> Optional[RiderTenant]:
        stmt = select(RiderTenant).where(
            RiderTenant.tenant_id == tenant_id,
            RiderTenant.rider_id == rider_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_riders_for_tenant(self, tenant_id: UUID) -> List[RiderTenant]:
        stmt = select(RiderTenant).where(RiderTenant.tenant_id == tenant_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_tenants_for_rider(self, rider_id: UUID) -> List[RiderTenant]:
        stmt = select(RiderTenant).where(RiderTenant.rider_id == rider_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def assign_rider(self, tenant_id: UUID, rider_id: UUID) -> RiderTenant:
        """
        Assign rider to tenant if not already assigned.
        """
        mapping = await self.get_mapping(tenant_id, rider_id)
        if mapping:
            return mapping  # silently return existing mapping

        data = RiderTenantCreate(tenant_id=tenant_id, rider_id=rider_id)
        return await self.create(data)

    async def remove_rider(self, tenant_id: UUID, rider_id: UUID) -> bool:
        """
        Remove rider from tenant.
        """
        mapping = await self.get_mapping(tenant_id, rider_id)
        if not mapping:
            return False

        await self.session.delete(mapping)
        await self.session.commit()
        return True

    async def list_tenant_riders(self, tenant_id: UUID) -> List[RiderTenant]:
        """
        List all riders assigned to a tenant.
        """
        return await self.get_riders_for_tenant(tenant_id)

    async def list_rider_tenants(self, rider_id: UUID) -> List[RiderTenant]:
        """
        List all tenants a rider belongs to.
        """
        return await self.get_tenants_for_rider(rider_id)
