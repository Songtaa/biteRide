from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import BaseRepository
from app.domains.public.models.payment_gateway import PaymentGatewayConfig
from app.domains.public.schemas.payment_gateway import (
    PaymentGatewayCreate, PaymentGatewayUpdate
)


class PaymentGatewayRepository(
    BaseRepository[PaymentGatewayConfig, PaymentGatewayCreate, PaymentGatewayUpdate]
):
    def __init__(self, session: AsyncSession):
        super().__init__(PaymentGatewayConfig, session)

    async def get_by_provider(
        self,
        tenant_id: UUID,
        provider: str
    ) -> Optional[PaymentGatewayConfig]:
        stmt = select(PaymentGatewayConfig).where(
            PaymentGatewayConfig.tenant_id == tenant_id,
            PaymentGatewayConfig.provider == provider,
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_tenant_gateways(
        self,
        tenant_id: UUID
    ) -> List[PaymentGatewayConfig]:
        stmt = select(PaymentGatewayConfig).where(
            PaymentGatewayConfig.tenant_id == tenant_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
