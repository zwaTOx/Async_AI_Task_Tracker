from typing import List
from fastapi import APIRouter, Depends, status

from src.database import DbSession
from src.task.dependencies import verify_update_task_perms
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_member, verify_create_task_perms
from .service import TaskService
from .schemas import TaskCreate, TaskPagination, TaskResponse, TaskUpdate

task_router = APIRouter()

@task_router.get(
    "/{project_id}/tasks",
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
    "/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse,
    dependencies=[Depends(verify_project_member), Depends(verify_create_task_perms)]
)
async def create_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_create: TaskCreate
):
    new_task = await TaskService(session).create_task(user.id, project_id, task_create)
    return new_task

@task_router.patch(
    "/{project_id}/tasks/{task_id}",
    dependencies=[Depends(verify_project_member), Depends(verify_update_task_perms)],
    response_model=TaskResponse
)
async def update_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    task_update: TaskUpdate
):
    upd_task = await TaskService(session).update_task(user.id, project_id, task_id, task_update)
    return upd_task

@task_router.delete(
    "/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_project_member), Depends(verify_update_task_perms)]
)
async def delete_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
):
    await TaskService(session).delete_task(user.id, project_id, task_id)