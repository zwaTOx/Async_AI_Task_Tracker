from sqlalchemy.ext.asyncio.session import AsyncSession
from .repository import IdeaRepository
from src.theme.repository import ThemeRepository
from .schemes import IdeaCreateRequest
from src.exceptions import NotFoundException, BadRequestException

class IdeaService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_theme_ideas(self,
        user_id: int, 
        project_id: int, 
        theme_id: int, 
    ):
        theme = await ThemeRepository(self.session).get(theme_id)
        if not theme:
            raise NotFoundException('Тема не найдена')
        ideas = await IdeaRepository(self.session).get_all(project_id=project_id, theme_id=theme_id)
        return ideas

    async def create_idea(self, 
        user_id: int, 
        project_id: int, 
        theme_id: int, 
        idea_data: IdeaCreateRequest
    ):
        theme = await ThemeRepository(self.session).get(theme_id)
        if not theme:
            raise NotFoundException('Тема не найдена')
        if theme.stage != "Brainshtorm":
            raise BadRequestException(f'Добавление идей недоступно. Сейчас {theme.stage}')
        new_idea = await IdeaRepository(self.session).create(idea_data, owner_id=user_id, project_id=project_id, theme_id=theme_id)
        return new_idea