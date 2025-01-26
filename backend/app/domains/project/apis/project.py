from typing import Any, List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from db.session import get_db
from domains.auth.models.users import User
from utils.rbac import get_current_user
from domains.project.schemas import project as schemas
from domains.project.services.project import project_service as actions

project_router = APIRouter()


@project_router.get(
    "/projects",
    response_model=List[schemas.ProjectSchema],
    tags=["project"]
)
async def list_projects(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100
) -> Any:
    projects = await actions.list_projects(db=db, skip=skip, limit=limit)
    return projects


@project_router.post(
    "/projects",
    response_model=schemas.ProjectSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["project"]
)
async def create_project(
        *, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        project_in: schemas.ProjectCreate
) -> Any:
    project = await actions.create_project(db=db, project_in=project_in)
    return project


@project_router.put(
    "/projects/{id}",
    response_model=schemas.ProjectSchema,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    tags=["project"],
)
async def update_project(
        *, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        id: UUID4,
        project_in: schemas.ProjectUpdate,
) -> Any:
    project = await actions.update_project(db=db, id=id, project_in=project_in)
    return project


@project_router.get(
    "/projects/{id}",
    response_model=schemas.ProjectSchema,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    tags=["project"],
)
async def get_project(
        *, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        id: UUID4
) -> Any:
    project = await actions.get_project(db=db, id=id)
    return project


@project_router.delete(
    "/projects/{id}",
    response_model=schemas.ProjectSchema,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    tags=["project"],
)
async def delete_project(
        *, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        id: UUID4
) -> Any:
    project = await actions.delete_project(db=db, id=id)
    return project
