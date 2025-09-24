from fastapi import APIRouter, Depends, Query, Request, status

from src.config import settings
from src.database import DbSession
from src.user.dependencies import CurrentUser
from .service import ProjectAssociationService
from .schemes import InviteModel
from .dependencies import verify_project_admin, vefify_project_member

user_project_as_router = APIRouter()

@user_project_as_router.get(
    "{project_id}/members",
    dependencies=[Depends(vefify_project_member)]
)
async def get_project_members(
    session: DbSession,
    user: CurrentUser,
    project_id: int
):
    members = await ProjectAssociationService(session).get_project_members(
        user.id, project_id
    )
    return members

@user_project_as_router.post(
    "{project_id}/members/invite",
    dependencies=[Depends(verify_project_admin)],
    status_code=status.HTTP_201_CREATED 
)
async def invite_user(
    session: DbSession,
    user: CurrentUser,
    request: Request,
    project_id: int,
    inv_data: InviteModel = Query(...)
):
    await ProjectAssociationService(session).invite_member_by_email(
        user, project_id, inv_data.email, inv_data.role
    )
    return {
        "message": "Приглашение в проект успешно отправлено"
    }

@user_project_as_router.post(
    "/members/confirm",
    status_code=status.HTTP_201_CREATED 
)
async def confirm_invite(
    session: DbSession,
    invite_token: str
):
    project_data = await ProjectAssociationService(session).confirm_invite(invite_token)
    return project_data

@user_project_as_router.delete(
    "{project_id}/members/{user_id}",
    dependencies=[Depends(verify_project_admin)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_member(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    user_id: int
):
    await ProjectAssociationService(session).delete_project_member(
        user.id,
        project_id,
        user_id
    )

@user_project_as_router.delete(
    "{project_id}/leave",
    dependencies=[Depends(vefify_project_member)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def leave_project(
    session: DbSession,
    user: CurrentUser,
    project_id: int
):
    await ProjectAssociationService(session).leave_project(user.id, project_id)