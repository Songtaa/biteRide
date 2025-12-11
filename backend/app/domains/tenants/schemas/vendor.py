from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import SQLModel


class VendorBase(SQLModel):
    name: str
    logo: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None


class VendorRead(VendorBase):
    id: UUID
    tenant_id: UUID
    is_deleted: bool
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
