from datetime import timedelta, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from src.database import DbSession
from src.role.dependencies import can_manage_task, can_view_task, can_create_task
from src.user.dependencies import CurrentUser
from .service import TaskService
from .schemas import TaskCreate, TaskPagination, TaskResponse, TaskResponseWithSubtasks, TaskUpdate
from src.websocket.manager import ws_manager

task_router = APIRouter()

@task_router.get(
    "/{project_id}/tasks",
    response_model=TaskPagination
)
async def get_project_tasks(
    session: DbSession,
    bg_task: BackgroundTasks,
    user: CurrentUser,
    project_id: int,
    _ = Depends(can_view_task)
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
    response_model=TaskResponseWithSubtasks
)
async def get_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    _ = Depends(can_view_task)
):
    task =  await TaskService(session).get_task_by_id(project_id, task_id)
    return task

@task_router.post(
    "/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
async def create_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_create: TaskCreate,
    _ = Depends(can_create_task)
):
    new_task = await TaskService(session).create_task(user.id, project_id, task_create)
    return new_task

@task_router.patch(
    "/{project_id}/tasks/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    task_update: TaskUpdate,
    _ = Depends(can_manage_task)
):
    upd_task = await TaskService(session).update_task(user.id, project_id, task_id, task_update)
    return upd_task

@task_router.delete(
    "/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    _ = Depends(can_manage_task)
):
    await TaskService(session).delete_task(user.id, project_id, task_id)