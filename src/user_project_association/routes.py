from fastapi import APIRouter, Request

from src.database import DbSession
from src.user.dependencies import CurrentUser
from .service import ProjectAssociationService
from .schemes import InviteModel

user_project_as_router = APIRouter()

@user_project_as_router.get(
    "{project_id}/members"
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
    "{project_id}/members"
)
async def invite_user(
    session: DbSession,
    user: CurrentUser,
    request: Request,
    project_id: int,
    invitation_request: InviteModel
):
    await ProjectAssociationService(session).invite_member_by_email(
        request, user, project_id, invitation_request
    )
    return 2