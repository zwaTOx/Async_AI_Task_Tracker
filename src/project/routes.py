from fastapi import APIRouter, status

from src.database import DbSession
from src.user.dependencies import CurrentUser
from .schemes import ProjectCreate, ProjectResponse, ProjectPagination
from .repository import ProjectRepository

project_router = APIRouter()


@project_router.get(
    "",
    response_model=ProjectPagination
)
async def get_projects(
    session: DbSession,
    user: CurrentUser,
):
    projects = await ProjectRepository(session).get_projects(user.id)
    return {"items" :projects}

@project_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectResponse
)
async def create_project(
    session: DbSession,
    user: CurrentUser,
    project_create_data: ProjectCreate
):
    new_project = await ProjectRepository(session).create_project(
        user.id, project_create_data
    )
    return new_project

