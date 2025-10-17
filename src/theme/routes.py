from fastapi import APIRouter, Depends, status
from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_member, verify_project_admin
from .schemes import ThemeCreate, ThemeUpdate
from .service import ThemeService
from .dependencies import verify_theme_in_project

theme_router = APIRouter()

@theme_router.get(
    "{project_id}/themes",
    dependencies=[Depends(verify_project_member)],
)
async def get_project_themes(
    session: DbSession,
    user: CurrentUser,
    project_id: int
):
    themes = await ThemeService(session).get_project_themes(project_id)
    return {"items": themes}

@theme_router.post(
    "{project_id}/themes",
    dependencies=[Depends(verify_project_admin)],
    status_code=status.HTTP_201_CREATED
)
async def create_theme(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_data: ThemeCreate
):
    new_theme = await ThemeService(session).create_theme(user.id, project_id, theme_data)
    return new_theme

@theme_router.patch(
    "{project_id}/themes/{theme_id}",
    dependencies=[Depends(verify_project_admin), Depends(verify_theme_in_project)]
)
async def update_theme(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int,
    theme_data: ThemeUpdate
):
    upd_theme = await ThemeService(session).update_theme(project_id, theme_id, theme_data)
    return upd_theme

@theme_router.delete(
    "{project_id}/themes/{theme_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_project_admin), Depends(verify_theme_in_project)]
)
async def delete_theme(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int,
):
    await ThemeService(session).delete_theme(project_id, theme_id)