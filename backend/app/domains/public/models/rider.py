from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import registry, mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime
from app.db.base_class import APIBase



class Rider(APIBase):
    __tablename__ = "riders"
    __table_args__ = {"schema": "public"}

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="offline")
    current_location: Mapped[Optional[str]] = mapped_column(String(255))

    tenants: Mapped[List["Tenant"]] = relationship(
        secondary="rider_tenant_link",
        back_populates="riders",
    )  
