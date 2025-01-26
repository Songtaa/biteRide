from sqlalchemy import (
    String, DateTime, Text, Enum
)
from sqlalchemy.orm import Mapped, mapped_column 
from enum import Enum as PyEnum 

from db.base_class import APIBase


class ProjectProgress(PyEnum):
    PLANNING = 'PLANNING'
    IN_PROGRESS = 'IN_PROGRESS'
    PAUSED = 'PAUSED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Project(APIBase):
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    progress: Mapped[ProjectProgress | None] = mapped_column(default=ProjectProgress.PLANNING)
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
