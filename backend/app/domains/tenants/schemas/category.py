from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from sqlmodel import SQLModel



class CategoryBase(SQLModel):
    name: str = Field(..., max_length=120)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    name: str | None = Field(None, max_length=120)
    description: str | None = None


class CategoryRead(CategoryBase):
    id: UUID
    tenant_id: UUID
    is_deleted: bool
    deleted_at: datetime | None

    class Config:
        from_attributes = True
