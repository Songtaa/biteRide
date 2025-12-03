from typing import List, Optional
from uuid import UUID
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.base import BaseRepository

from app.domains.public.models.rider_tenant_link import RiderTenantLink
from app.domains.public.schemas.rider_tenant import RiderTenantCreate


class RiderTenantRepository(BaseRepository[RiderTenantLink, RiderTenantCreate, dict]):

    def __init__(self, session: AsyncSession):
        super().__init__(RiderTenantLink, session)


    async def get_mapping(self, tenant_id: UUID, rider_id: UUID) -> Optional[RiderTenantLink]:
        stmt = select(RiderTenantLink).where(
            RiderTenantLink.tenant_id == tenant_id,
            RiderTenantLink.rider_id == rider_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_riders_for_tenant(self, tenant_id: UUID) -> List[RiderTenantLink]:
        stmt = select(RiderTenantLink).where(RiderTenantLink.tenant_id == tenant_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_tenants_for_rider(self, rider_id: UUID) -> List[RiderTenantLink]:
        stmt = select(RiderTenantLink).where(RiderTenantLink.rider_id == rider_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def assign_rider(self, tenant_id: UUID, rider_id: UUID) -> RiderTenantLink:
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

    async def list_tenant_riders(self, tenant_id: UUID) -> List[RiderTenantLink]:
        """
        List all riders assigned to a tenant.
        """
        return await self.get_riders_for_tenant(tenant_id)

    async def list_rider_tenants(self, rider_id: UUID) -> List[RiderTenantLink]:
        """
        List all tenants a rider belongs to.
        """
        return await self.get_tenants_for_rider(rider_id)
