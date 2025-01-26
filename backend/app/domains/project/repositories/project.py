from crud.base import CRUDBase
from domains.project.models.project import Project
from domains.project.schemas.project import (
    ProjectCreate, ProjectUpdate
)


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


project_actions = CRUDProject(Project)
