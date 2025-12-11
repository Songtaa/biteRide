# app/domains/tenants/repository/vendor.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.tenants.models.vendor import Vendor
from app.domains.tenants.schemas.vendor import VendorCreate, VendorUpdate


from app.crud.base import BaseRepository

from datetime import datetime



class VendorRepository(BaseRepository[Vendor, VendorCreate, VendorUpdate]):
    
    def __init__(self, session: AsyncSession):
        super().__init__(Vendor, session)
        self.session = session

    async def get_by_tenant(self, vendor_id: int, tenant_id: int) -> Optional[Vendor]:
        query = (
            select(Vendor)
            .where(
                Vendor.id == vendor_id,
                Vendor.tenant_id == tenant_id
            )
        )
        return await self.session.scalar(query)

    async def list_by_tenant(self, tenant_id: int) -> List[Vendor]:
        query = (
            select(Vendor)
            .where(
                Vendor.tenant_id == tenant_id,
                Vendor.is_deleted == False
            )
        )
        result = await self.session.scalars(query)
        return result.all()

    async def soft_delete(self, vendor: Vendor):
        vendor.is_deleted = True
        vendor.deleted_at = datetime.now()
        await self.session.flush()
        return vendor

    async def restore(self, vendor: Vendor):
        vendor.is_deleted = False
        vendor.deleted_at = None
        await self.session.flush()
        return vendor


