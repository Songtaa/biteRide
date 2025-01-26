from typing import List

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from domains.project.repositories.project import project_actions as project_repo
from domains.project.schemas.project import ProjectSchema, ProjectUpdate, ProjectCreate


class ProjectService:

    def __init__(self):
        self.repo = project_repo

    async def list_projects(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[ProjectSchema]:
        projects = self.repo.get_all(db=db, skip=skip, limit=limit)
        return projects

    async def create_project(self, *, db: Session, project_in: ProjectCreate) -> ProjectSchema:
        project = await self.repo.create(db=db, obj_in=project_in)
        return project

    async def update_project(self, *, db: Session, id: UUID4, project_in: ProjectUpdate) -> ProjectSchema:
        project = self.repo.get(db=db, id=id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        project = self.repo.update(db=db, db_obj=project, obj_in=project_in)
        return project

    async def get_project(self, *, db: Session, id: UUID4) -> ProjectSchema:
        project = self.repo.get(db=db, id=id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def delete_project(self, *, db: Session, id: UUID4) -> ProjectSchema:
        project = self.repo.get(db=db, id=id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        project = self.repo.remove(db=db, id=id)
        return project

    async def get_project_by_id(self, *, db: Session, id: UUID4) -> ProjectSchema:
        project = self.repo.get(db=db, id=id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project


project_service = ProjectService()
