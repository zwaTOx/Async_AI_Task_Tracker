from fastapi import APIRouter, status
from src.database import DbSession
from src.user.dependencies import CurrentUser
from .service import VoteService

vote_router = APIRouter()

@vote_router.post(
    "/{project_id}/themes/{theme_id}/ideas/{idea_id}/voites",
    status_code=status.HTTP_201_CREATED
)
async def vote_idea(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int,
    idea_id: int
):
    vote = await VoteService(session).vote(user.id, theme_id, idea_id)
    return vote

@vote_router.delete(
    "/{project_id}/themes/{theme_id}/ideas/{idea_id}/voites",
    status_code=status.HTTP_204_NO_CONTENT
)
async def unvote(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int,
    idea_id: int
):
    await VoteService(session).unvote(user.id, theme_id, idea_id)