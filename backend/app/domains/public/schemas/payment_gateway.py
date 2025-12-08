from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel



class PaymentGatewayBase(SQLModel):
    provider: str = Field(..., examples=["mtn_momo", "hubtel", "stripe"])
    public_key: str
    secret_key: str
    is_sandbox: bool = True
    metadata_json: Optional[dict] = None


class PaymentGatewayCreate(PaymentGatewayBase):
    pass


class PaymentGatewayUpdate(BaseModel):
    public_key: Optional[str] = None
    secret_key: Optional[str] = None
    is_sandbox: Optional[bool] = None
    metadata_json: Optional[dict] = None

class PaymentGatewayOut(PaymentGatewayBase):
    id: UUID
    tenant_id: UUID

    model_config = {"from_attributes": True}
