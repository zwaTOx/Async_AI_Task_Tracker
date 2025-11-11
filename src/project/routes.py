from fastapi import APIRouter, Depends, status

from src.database import DbSession
from src.role.dependencies import can_delete_project, can_view_project, can_edit_project
from src.user.dependencies import CurrentUser
from .schemes import ProjectCreate, ProjectResponse, ProjectPagination, ProjectUpdate
from .repository import ProjectRepository
from .service import ProjectService
from src.user_project_association.dependencies import Action
from .dependency import verify_project_action
from src.user_project_association.dependencies import verify_project_admin

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
    new_project = await ProjectService(session).create_project(
        user.id, project_create_data
    )
    return new_project

@project_router.patch(
    "/{project_id}"
)
async def update_project(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    project_update_data: ProjectUpdate,
    _ = Depends(can_edit_project())
):
    updated_project = await ProjectService(session).update_project(
        user.id, project_id, project_update_data
    )
    return updated_project

@project_router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    _ = Depends(can_delete_project())
):
    await ProjectService(session).delete_project(user.id, project_id)