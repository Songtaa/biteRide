from datetime import datetime
from typing import Optional

from domains.project.models.project import ProjectProgress
from pydantic import BaseModel
from pydantic import UUID4


# Project
class ProjectBase(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    progress: Optional[ProjectProgress] = None
    timestamp: Optional[datetime] = None


# Properties to receive via API on creation
class ProjectCreate(ProjectBase):
    title: str
    description: str


# Properties to receive via API on update
class ProjectUpdate(ProjectBase):
    pass


class ProjectInDBBase(ProjectBase):
    id: Optional[UUID4] = None
    creator_id: Optional[UUID4] = None
    updator_id: Optional[UUID4] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class ProjectSchema(ProjectInDBBase):
    pass
