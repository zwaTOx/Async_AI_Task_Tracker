from fastapi import APIRouter, Query, Request, status

from src.config import settings
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
    "{project_id}/members/invite",
    status_code=status.HTTP_201_CREATED 
)
async def invite_user(
    session: DbSession,
    user: CurrentUser,
    request: Request,
    project_id: int,
    inv_email: str = Query(...),
    inv_role: str = Query(default=settings.DEFAULT_PROJECT_ROLE)
):
    await ProjectAssociationService(session).invite_member_by_email(
        request, user, project_id, inv_email, inv_role
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