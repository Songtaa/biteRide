# app/domains/tenants/services/category.py

from uuid import UUID
from typing import List
from fastapi import HTTPException, status

from app.domains.tenants.repository.category import CategoryRepository
from app.domains.tenants.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)
from app.domains.tenants.models.category import Category


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, tenant_id: UUID, data: CategoryCreate) -> Category:
        # Prevent duplicate names
        existing = await self.repo.get_by_name(data.name, tenant_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category '{data.name}' already exists"
            )

        payload = data.model_dump()
        payload["tenant_id"] = tenant_id

        return await self.repo.create(payload)

    async def get_category(self, category_id: UUID, tenant_id: UUID) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category or category.tenant_id != tenant_id or category.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    async def list_categories(self, tenant_id: UUID, skip: int, limit: int) -> List[Category]:
        return await self.repo.list_categories(tenant_id, skip, limit)

    async def update_category(
        self,
        category_id: UUID,
        tenant_id: UUID,
        data: CategoryUpdate
    ) -> Category:
        category = await self.get_category(category_id, tenant_id)
        return await self.repo.update(db_obj=category, obj_in=data)

    async def soft_delete_category(self, category_id: UUID, tenant_id: UUID) -> dict:
        deleted = await self.repo.soft_delete(category_id, tenant_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"status": "deleted"}

    async def hard_delete_category(self, category_id: UUID, tenant_id: UUID) -> dict:
        deleted = await self.repo.hard_delete(category_id, tenant_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"status": "permanently_removed"}
