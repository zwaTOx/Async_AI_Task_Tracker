from typing import List
from fastapi import APIRouter, Depends, status

from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_member
from .service import TaskService
from .schemas import TaskCreate, TaskPagination, TaskResponse

task_router = APIRouter()

@task_router.get(
    "/{project_id}",
    response_model=TaskPagination,
    dependencies=[Depends(verify_project_member)]
)
async def get_project_tasks(
    session: DbSession,
    user: CurrentUser,
    project_id: int
):
    tasks = await TaskService(session).get_tasks(project_id)
    return {"items" :tasks}

@task_router.post(
    "/{project_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_project_member)]
)
async def create_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_create: TaskCreate
):
    new_task = await TaskService(session).create_task(user.id, project_id, task_create)
    return new_task