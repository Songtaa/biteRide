# app/domains/tenants/repository/category.py

from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseRepository
from app.domains.tenants.models.category import Category
from app.domains.tenants.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_name(self, name: str, tenant_id: UUID) -> Optional[Category]:
        stmt = (
            select(Category)
            .where(Category.name == name)
            .where(Category.tenant_id == tenant_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_categories(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Category]:
        stmt = (
            select(Category)
            .where(Category.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, category_id: UUID, tenant_id: UUID) -> bool:
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .where(Category.tenant_id == tenant_id)
            .where(Category.is_deleted == False)
        )
        result = await self.session.execute(stmt)
        category = result.scalars().first()

        if not category:
            return False

        category.is_deleted = True
        self.session.add(category)
        await self.session.commit()
        return True

    async def hard_delete(self, category_id: UUID, tenant_id: UUID) -> bool:
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .where(Category.tenant_id == tenant_id)
        )
        result = await self.session.execute(stmt)
        category = result.scalars().first()

        if not category:
            return False

        await self.session.delete(category)
        await self.session.commit()
        return True
