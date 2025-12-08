from uuid import UUID, uuid4
from typing import Optional

from sqlalchemy import String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.db.base_class import Base  # your declarative base
from app.domains.public.models.tenant import Tenant
from app.db.base_class import APIBase



class PaymentGatewayConfig(APIBase):
    """
    Tenant-level Payment Gateway Configuration Model
    """
    __tablename__ = "payment_gateway_configs"
    __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey("public.tenants.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    public_key: Mapped[str] = mapped_column(String(255), nullable=False)
    secret_key: Mapped[str] = mapped_column(String(255), nullable=False)

    is_sandbox: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="payment_configs")
