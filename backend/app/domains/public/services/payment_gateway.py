from uuid import UUID
from typing import List

from app.domains.public.repository.payment_gateway import (
    PaymentGatewayRepository
)
from app.domains.public.schemas.payment_gateway import (
    PaymentGatewayCreate,
    PaymentGatewayUpdate,
    PaymentGatewayOut
)
from app.utils.errors import NotFoundException, BadRequestException


class PaymentGatewayService:

    def __init__(self, repo: PaymentGatewayRepository):
        self.repo = repo

    async def create_gateway(
        self,
        tenant_id: UUID,
        data: PaymentGatewayCreate
    ) -> PaymentGatewayOut:

        # prevent duplicate provider config
        existing = await self.repo.get_by_provider(tenant_id, data.provider)
        if existing:
            raise BadRequestException("Provider already configured for this tenant.")

        obj = await self.repo.create(
            data.model_dump(),
            extra={"tenant_id": tenant_id}
        )
        return obj

    async def update_gateway(
        self,
        tenant_id: UUID,
        gateway_id: UUID,
        data: PaymentGatewayUpdate
    ) -> PaymentGatewayOut:

        obj = await self.repo.get(gateway_id)
        if not obj or obj.tenant_id != tenant_id:
            raise NotFoundException("Gateway config not found.")

        return await self.repo.update(gateway_id, data.model_dump(exclude_unset=True))

    async def list_gateways(self, tenant_id: UUID) -> List[PaymentGatewayOut]:
        return await self.repo.list_tenant_gateways(tenant_id)

    async def delete_gateway(self, tenant_id: UUID, gateway_id: UUID) -> None:
        obj = await self.repo.get(gateway_id)
        if not obj or obj.tenant_id != tenant_id:
            raise NotFoundException("Gateway config not found.")
        await self.repo.delete(gateway_id)
