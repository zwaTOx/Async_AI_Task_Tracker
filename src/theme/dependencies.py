from src.database import DbSession
from src.exceptions import NotFoundException
from src.user.dependencies import CurrentUser
from .repository import ThemeRepository

async def verify_theme_in_project(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    theme_id: int
):
    theme = await ThemeRepository(session).get(theme_id)
    if theme is None or theme.project_id!=project_id:
        raise NotFoundException('Тема не найдена в проекте')
    