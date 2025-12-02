from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class RoleBase(BaseModel):
    name: str
    

class RoleCreate(RoleBase):
    description: str | None = None

class RoleUpdate(BaseModel):
    name: Optional[str] | None = None
    description: Optional[str] | None = None

class RoleRead(RoleCreate):
    id: UUID
    
    
    class Config:
        orm_mode = True
    
class RoleSchema(RoleRead):
    pass

# class PermissionCreate(BaseModel):
#     name: str

# class PermissionRead(BaseModel):
#     id: UUID
#     name: str

# class RoleWithPermissions(RoleRead):
#     permissions: List[PermissionRead] = []
