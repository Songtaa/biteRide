# app/domains/tenants/services/vendor.py
from typing import List
from uuid import UUID
from fastapi import HTTPException, status

from app.domains.tenants.repository.vendor import VendorRepository
from app.domains.tenants.schemas.vendor import VendorCreate, VendorUpdate, VendorRead


from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.tenant_dependencies import get_tenant_id_from_context



class VendorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = VendorRepository(session)

    async def create_vendor(self, data: VendorCreate):
        tenant_id = get_tenant_id_from_context()
        vendor = await self.repo.create(tenant_id, data)
        await self.session.commit()
        return vendor

    async def get_vendor(self, vendor_id: int):
        tenant_id = get_tenant_id_from_context()
        vendor = await self.repo.get(vendor_id, tenant_id)

        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        return vendor

    async def list_vendors(self):
        tenant_id = get_tenant_id_from_context()
        return await self.repo.list(tenant_id)

    async def update_vendor(self, vendor_id: int, data: VendorUpdate):
        vendor = await self.get_vendor(vendor_id)
        vendor = await self.repo.update(vendor, data)
        await self.session.commit()
        return vendor

    async def soft_delete_vendor(self, vendor_id: int):
        vendor = await self.get_vendor(vendor_id)
        await self.repo.soft_delete(vendor)
        await self.session.commit()
        return {"message": "Vendor soft-deleted"}

    async def restore_vendor(self, vendor_id: int):
        vendor = await self.get_vendor(vendor_id)
        await self.repo.restore(vendor)
        await self.session.commit()
        return {"message": "Vendor restored"}

    async def hard_delete_vendor(self, vendor_id: int):
        vendor = await self.get_vendor(vendor_id)
        await self.repo.hard_delete(vendor)
        await self.session.commit()
        return {"message": "Vendor permanently deleted"}
