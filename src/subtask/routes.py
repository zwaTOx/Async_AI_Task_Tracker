from fastapi import APIRouter, Depends, status

from src.role.dependencies import can_view_task, can_manage_task
from src.user.dependencies import CurrentUser
from src.database import DbSession
from .service import SubtaskService
from .schemas import SubtaskResponse, SubtaskPargination, SubtaskCreate, SubtaskUpdate

subtask_router = APIRouter()

@subtask_router.get(
    "/projects/{project_id}/tasks/{task_id}/subtasks",
    response_model=SubtaskPargination
)
async def get_task_subtasks(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    _ = Depends(can_view_task)
):
    subtasks = await SubtaskService(session).get_subtasks(task_id)
    return {"items": subtasks}

@subtask_router.post(
    "/projects/{project_id}/tasks/{task_id}/subtasks",
    status_code=status.HTTP_201_CREATED,
    response_model=SubtaskResponse
)
async def create_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_data: SubtaskCreate,
    _ = Depends(can_manage_task)
):
    new_subtask = await SubtaskService(session).create_subtask(task_id, subtask_data)
    return new_subtask

@subtask_router.patch(
    "/projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}",
    response_model=SubtaskResponse
)
async def update_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_id: int,
    subtask_data: SubtaskUpdate,
    _ = Depends(can_manage_task)
):
    upd_subtask = await SubtaskService(session).update_subtask(subtask_id, subtask_data)
    return upd_subtask

@subtask_router.delete(
    "/projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_id: int,
    _ = Depends(can_manage_task)
):
    await SubtaskService(session).delete_subtask(subtask_id)