from fastapi import APIRouter

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
    ProjectAssociationService(session).get_project_members(
        user.id, project_id
    )

@user_project_as_router.post(
    "{project_id}/members"
)
async def invite_user(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    invitation_request: InviteModel
):
    pass