# app/domains/tenants/apis/category.py

from typing import Annotated, AsyncGenerator, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.tenant_dependencies import get_tenant_id_from_context
from app.db.session import get_tenant_session

from app.domains.tenants.repository.category import CategoryRepository
from app.domains.tenants.services.category import CategoryService
from app.domains.tenants.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
)


category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


async def get_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_tenant_session() as session:
        yield session


def get_category_service(
    session: AsyncSession = Depends(get_session_dep),
):
    repo = CategoryRepository(session)
    return CategoryService(repo)


ServiceDep = Annotated[CategoryService, Depends(get_category_service)]
TenantID = Annotated[UUID, Depends(get_tenant_id_from_context)]

@category_router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="TenantCategoryCreate",
)
async def create_category(
    data: CategoryCreate,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.create_category(tenant_id, data)


@category_router.get(
    "/{category_id}",
    response_model=CategoryRead,
    operation_id="TenantCategoryGet",
)
async def get_category(
    category_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.get_category(category_id, tenant_id)


@category_router.get(
    "",
    response_model=List[CategoryRead],
    operation_id="TenantCategoryList",
)
async def list_categories(
    tenant_id: TenantID,
    service: ServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    return await service.list_categories(tenant_id, skip, limit)


@category_router.put(
    "/{category_id}",
    response_model=CategoryRead,
    operation_id="TenantCategoryUpdate",
)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.update_category(category_id, tenant_id, data)


@category_router.delete(
    "/{category_id}/soft",
    operation_id="TenantCategorySoftDelete",
)
async def soft_delete_category(
    category_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.soft_delete_category(category_id, tenant_id)


@category_router.delete(
    "/{category_id}/hard",
    operation_id="TenantCategoryHardDelete",
)
async def hard_delete_category(
    category_id: UUID,
    tenant_id: TenantID,
    service: ServiceDep,
):
    return await service.hard_delete_category(category_id, tenant_id)
