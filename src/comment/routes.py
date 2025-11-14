from fastapi import APIRouter, Depends, status
from src.database import DbSession
from src.task.dependencies import verify_task_action
from src.user.dependencies import CurrentUser

from .service import CommentService
from .schemes import CommentCreate, CommentResponse, CommentPargination, CommentUpdate, PaginationParams
from .dependencies import verify_comment_creation, verify_comment_modification, Action

task_comment_router = APIRouter()

@task_comment_router.get(
    "/{project_id}/tasks/{task_id}/comments",
    dependencies=[
        Depends(verify_task_action(action=Action.VIEW))
    ],
    response_model=CommentPargination
)
async def get_task_comments(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    pagination: PaginationParams = Depends()
):
    comments = await CommentService(session).get_comments(task_id, pagination)
    return {'params': pagination, 'items': comments}

@task_comment_router.post(
    "/{project_id}/tasks/{task_id}/comments",
    dependencies=[
        Depends(verify_task_action(action=Action.VIEW)),
        Depends(verify_comment_creation())
    ],
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
async def post_comment(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    comment_data: CommentCreate,
    comment_id: int = None
):
    new_comment = await CommentService(session).create_comment(user.id, task_id, comment_id, comment_data)
    return new_comment

@task_comment_router.patch(
    "/{project_id}/tasks/{task_id}/comments/{comment_id}",
    dependencies=[
        Depends(verify_task_action(action=Action.VIEW)),
        Depends(verify_comment_modification(Action.EDIT))
    ],
    response_model=CommentResponse,
)
async def update_comment(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    comment_id: int,
    comment_data: CommentUpdate
):
    new_comment = await CommentService(session).update_comment(comment_id, comment_data)
    return new_comment

@task_comment_router.delete(
    "/{project_id}/tasks/{task_id}/comments/{comment_id}",
    dependencies=[
        Depends(verify_task_action(action=Action.VIEW)),
        Depends(verify_comment_modification(Action.DELETE))
    ],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    task_id: int,
    comment_id: int,  
):
    await CommentService(session).delete_comment(comment_id)