from uuid import UUID
from sqlmodel import SQLModel
from sqlalchemy.orm import registry, mapped_column, Mapped
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


from app.db.base_class import APIBase




class RiderTenantLink(APIBase):
    __tablename__ = "rider_tenant_link"

    rider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("public.riders.id"), primary_key=True
    )

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("public.tenants.id"), primary_key=True
    )