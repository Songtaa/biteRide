from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_master_session

from app.domains.public.repository.payment_gateway import PaymentGatewayRepository
from app.domains.public.services.payment_gateway import PaymentGatewayService
from app.domains.public.schemas.payment_gateway import (
    PaymentGatewayCreate,
    PaymentGatewayUpdate,
    PaymentGatewayOut
)


payment_router = APIRouter(
    prefix="/payment-gateways",
    tags=["Payment Gateways"],
    responses={404: {"description": "Not found"}},
)



async def get_master_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_master_session() as session:
        yield session


def get_payment_service(
    session: AsyncSession = Depends(get_master_session_dep),
):
    repo = PaymentGatewayRepository(session)
    return PaymentGatewayService(repo)

ServiceDep = Annotated[PaymentGatewayService, Depends(get_payment_service)]



@payment_router.post(
    "/gateway",
    response_model=PaymentGatewayOut,
    status_code=status.HTTP_201_CREATED,
    operation_id="PaymentGatewayCreate"
)
async def create_gateway(
    data: PaymentGatewayCreate,
    service: ServiceDep,
):
    return await service.create(data)


@payment_router.get(
    "/{config_id}",
    response_model=PaymentGatewayOut,
    operation_id="PaymentGatewayGet"
)
async def get_gateway(
    config_id: UUID,
    service: ServiceDep,
):
    gateway = await service.get(config_id)
    if not gateway:
        raise HTTPException(404, "Payment gateway config not found")
    return gateway


@payment_router.put(
    "/{config_id}",
    response_model=PaymentGatewayOut,
    operation_id="PaymentGatewayUpdate"
)
async def update_gateway(
    config_id: UUID,
    data: PaymentGatewayUpdate,
    service: ServiceDep,
):
    updated = await service.update(config_id, data)
    if not updated:
        raise HTTPException(404, "Payment gateway config not found")
    return updated


@payment_router.delete(
    "/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="PaymentGatewayDelete"
)
async def delete_gateway(
    config_id: UUID,
    service: ServiceDep,
):
    deleted = await service.delete(config_id)
    if not deleted:
        raise HTTPException(404, "Payment gateway config not found")
    return None


@payment_router.get(
    "/",
    response_model=list[PaymentGatewayOut],
    operation_id="PaymentGatewayList"
)
async def list_gateways(
    service: ServiceDep,
):
    return await service.list_all()
