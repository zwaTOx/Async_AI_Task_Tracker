from fastapi import APIRouter, Depends, status

from src.task.dependencies import verify_update_task_perms
from src.user_project_association.dependencies import verify_project_member
from src.user.dependencies import CurrentUser
from src.database import DbSession
from .service import SubtaskService
from .schemas import SubtaskResponse, SubtaskPargination, SubtaskCreate, SubtaskUpdate

subtask_router = APIRouter( tags=["Subtasks"])

@subtask_router.get(
    "/projects/{project_id}/tasks/{task_id}/subtasks",
    dependencies=[Depends(verify_project_member)],
    response_model=SubtaskPargination
)
async def get_task_subtasks(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
):
    subtasks = await SubtaskService(session).get_subtasks(task_id)
    return {"items": subtasks}

@subtask_router.post(
    "/projects/{project_id}/tasks/{task_id}/subtasks",
    dependencies=[Depends(verify_project_member), Depends(verify_update_task_perms)],
    status_code=status.HTTP_201_CREATED,
    response_model=SubtaskResponse
)
async def create_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_data: SubtaskCreate
):
    new_subtask = await SubtaskService(session).create_subtask(task_id, subtask_data)
    return new_subtask

@subtask_router.patch(
    "projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}",
    dependencies=[Depends(verify_project_member), Depends(verify_update_task_perms)],
    response_model=SubtaskResponse
)
async def update_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_id: int,
    subtask_data: SubtaskUpdate
):
    upd_subtask = await SubtaskService(session).update_subtask(subtask_id, subtask_data)
    return upd_subtask

@subtask_router.delete(
    "projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}",
    dependencies=[Depends(verify_project_member), Depends(verify_update_task_perms)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_subtask(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    subtask_id: int
):
    await SubtaskService(session).delete_subtask(subtask_id)