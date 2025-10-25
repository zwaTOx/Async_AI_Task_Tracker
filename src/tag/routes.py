from fastapi import APIRouter, Depends, status

from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.tag.dependencies import verify_tag_action
from src.user_project_association.dependencies import Action
from .dependencies import verify_tag_exists, verify_tag_action
from .service import TagService
from .schemes import TagCreate, TagResponse, TagPargination, TagUpdate

tag_router = APIRouter()

@tag_router.get(
    "/{project_id}/tags",
    response_model=TagPargination,
    dependencies=[
        Depends(verify_tag_action(Action.VIEW))
    ],
)
async def get_project_tags(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
):
    tags = await TagService(session).get_project_tags(project_id)
    return {"items": tags}

@tag_router.post(
    "/{project_id}/tags",
    dependencies=[
        Depends(verify_tag_action(Action.CREATE))
    ],
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_tag(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    tag_data: TagCreate
):
    new_tag = await TagService(session).create_tag(project_id, tag_data)
    return new_tag

@tag_router.patch(
    "{project_id}/tags/{tag_id}",
    dependencies=[
        Depends(verify_tag_action(Action.EDIT))
    ], 
)
async def update_tag(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    tag_id: int,
    tag_data: TagUpdate
):
    tag_upd = await TagService(session).update_tag(tag_id, tag_data)
    return tag_upd

@tag_router.delete(
    "{project_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(verify_tag_action(Action.DELETE))
    ]
)    
async def delete_tag(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    tag_id: int,    
):
    await TagService(session).delete_tag(tag_id)