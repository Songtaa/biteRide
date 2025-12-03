from typing import List
from uuid import UUID
from fastapi import HTTPException

from app.domains.public.repository.rider_tenant import RiderTenantRepository
from app.domains.public.repository.rider import RiderRepository
from app.domains.public.repository.tenant import TenantRepository

from app.domains.public.schemas.rider_tenant import (
    RiderTenantCreate,
    RiderTenantRead
)


class RiderTenantService:

    def __init__(
        self,
        rider_tenant_repo: RiderTenantRepository,
        rider_repo: RiderRepository,
        tenant_repo: TenantRepository
    ):
        self.rider_tenant_repo = rider_tenant_repo
        self.rider_repo = rider_repo
        self.tenant_repo = tenant_repo


    async def _ensure_rider_exists(self, rider_id: UUID):
        rider = await self.rider_repo.get_by_id(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return rider

    async def _ensure_tenant_exists(self, tenant_id: UUID):
        tenant = await self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant

    async def assign_rider(self, tenant_id: UUID, rider_id: UUID) -> RiderTenantRead:
        await self._ensure_rider_exists(rider_id)
        await self._ensure_tenant_exists(tenant_id)

        mapping = await self.rider_tenant_repo.assign_rider(
            tenant_id=tenant_id,
            rider_id=rider_id
        )
        return mapping

    async def remove_rider(self, tenant_id: UUID, rider_id: UUID) -> bool:
        await self._ensure_rider_exists(rider_id)
        await self._ensure_tenant_exists(tenant_id)

        removed = await self.rider_tenant_repo.remove_rider(tenant_id, rider_id)
        if not removed:
            raise HTTPException(status_code=404, detail="Rider not assigned to tenant")

        return True

    async def list_tenant_riders(self, tenant_id: UUID):
        await self._ensure_tenant_exists(tenant_id)
        return await self.rider_tenant_repo.list_tenant_riders(tenant_id)

    async def list_rider_tenants(self, rider_id: UUID):
        await self._ensure_rider_exists(rider_id)
        return await self.rider_tenant_repo.list_rider_tenants(rider_id)
