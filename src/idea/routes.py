from fastapi import APIRouter, status, Depends
from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_action

from .service import IdeaService
from .schemes import IdeaCreateRequest

idea_router = APIRouter()

@idea_router.get(
    "/{project_id}/themes/{theme_id}/ideas",
    # dependencies=[Depends(verify_project_action(action='VIEW'))]
)
async def get_theme_ideas(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int
):
    ideas = await IdeaService(session).get_theme_ideas(user.id, project_id, theme_id)
    return {"items": ideas}

@idea_router.post(
    "/{project_id}/themes/{theme_id}/ideas",
    status_code=status.HTTP_201_CREATED
)
async def create_idea(
    session: DbSession,
    user: CurrentUser,
    project_id: int, 
    theme_id: int,
    idea_data: IdeaCreateRequest
):
    new_idea = await IdeaService(session).create_idea(user.id, project_id, theme_id, idea_data)
    return new_idea