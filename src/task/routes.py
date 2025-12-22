from datetime import timedelta, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
import asyncio

from src.database import DbSession
from src.task.dependencies import verify_task_action
from src.user_project_association.access_config import Action, ResourceType
from src.user.dependencies import CurrentUser
from .service import TaskService
from .schemas import TaskCreate, TaskPagination, TaskResponse, TaskResponseWithSubtasks, TaskUpdate
from src.attachment.schemes import AttachResponse
from src.websocket.manager import ws_manager

task_router = APIRouter()

@task_router.get(
    "/{project_id}/tasks",
    response_model=TaskPagination,
    dependencies=[
        Depends(verify_task_action(Action.VIEW))
    ],
)
async def get_project_tasks(
    session: DbSession,
    bg_task: BackgroundTasks,
    user: CurrentUser,
    project_id: int,
):
    tasks = await TaskService(session).get_tasks(project_id)
    bg_task.add_task(ws_manager.broadcast_to_project, project_id, {'action': "get_task", 'user_id': user.id})
    return {"items" :tasks}

@task_router.get(
    "/tasks",
    response_model=TaskPagination
)
async def get_all_tasks_by_date(
    session: DbSession,
    user: CurrentUser,
    date: datetime = Query(datetime.now(), description="Начальная дата"),
    days_after: int = Query(7, description="Количество дней после указанной даты", ge=0),
    project_ids: Optional[List[int]] = Query(None, description="ID проектов (опционально)")
):
    end_date = date + timedelta(days=days_after)
    
    tasks = await TaskService(session).get_tasks_by_date_range(
        user_id=user.id,
        project_ids=project_ids,
        start_date=date,
        end_date=end_date
    )
    return {"items" :tasks}

@task_router.get(
    "/{project_id}/tasks/{task_id}",
    response_model=TaskResponseWithSubtasks,
    dependencies=[
        Depends(verify_task_action(Action.VIEW))
    ],
)
async def get_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int
):
    task =  await TaskService(session).get_task_by_id(project_id, task_id)
    return task

@task_router.post(
    "/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse,
    dependencies=[
        Depends(verify_task_action(Action.CREATE))
    ]
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
    response_model=TaskResponse,
    dependencies=[
        Depends(verify_task_action(Action.EDIT))
    ],
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

@task_router.post(
    "/{project_id}/tasks/{task_id}/files",
    response_model=AttachResponse,
    dependencies=[
        Depends(verify_task_action(Action.EDIT))
    ],
)
async def pin_file_in_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    file_id: int
):
    file_info = await TaskService(session).pin_file(user.id, project_id, task_id, file_id)
    return file_info

@task_router.delete(
    "/{project_id}/tasks/{task_id}/files",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(verify_task_action(Action.EDIT))
    ],
)
async def unpin_file_in_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    file_id: int
):
    await TaskService(session).unpin_file(user.id, project_id, task_id, file_id)

@task_router.delete(
    "/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(verify_task_action(Action.DELETE))
    ]
)
async def delete_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
):
    await TaskService(session).delete_task(user.id, project_id, task_id)