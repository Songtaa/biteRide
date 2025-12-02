from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel


class RiderBase(SQLModel):
    full_name: str
    phone_number: str
    vehicle_type: str
    national_id: Optional[str] = None


class RiderCreate(RiderBase):
    pass


class RiderRead(RiderBase):
    id: UUID
    is_active: bool


class RiderUpdate(SQLModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    national_id: Optional[str] = None
    is_active: Optional[bool] = None
    

class RiderOut(RiderBase):
    id: UUID

    class Config:
        from_attributes = True