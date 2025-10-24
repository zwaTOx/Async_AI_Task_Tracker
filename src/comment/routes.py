from fastapi import APIRouter, Depends, status
from src.database import DbSession
from src.user.dependencies import CurrentUser

from .service import CommentService
from .schemes import CommentCreate, CommentResponse, CommentPargination

from src.user_project_association.dependencies import verify_project_member
from src.task.dependencies import verify_task_exists
task_comment_router = APIRouter()

@task_comment_router.get(
    "{project_id}/tasks/{tasks_id}/comments",
    dependencies=[Depends(verify_project_member), Depends(verify_task_exists)],
    response_model=CommentPargination
)
async def get_task_comments(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
):
    comments = await CommentService(session).get_comments(task_id)
    return {'items': comments}

@task_comment_router.post(
    "{project_id}/tasks/{tasks_id}/comments",
    dependencies=[Depends(verify_project_member)],
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
async def post_comment(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    comment_data: CommentCreate
):
    new_comment = await CommentService(session).create_comment(user.id, task_id, comment_data)
    return new_comment