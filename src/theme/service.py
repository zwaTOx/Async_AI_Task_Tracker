from sqlalchemy.ext.asyncio.session import AsyncSession
from src.exceptions import NotFoundException
from .repository import ThemeRepository
from .schemes import ThemeCreate, ThemeUpdate

class ThemeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_themes(self, project_id: int):
        result = await ThemeRepository(self.session).get_all(project_id=project_id)
        return result
    
    async def create_theme(self, owner_id: int, project_id: int, theme_data: ThemeCreate):
        new_theme = await ThemeRepository(self.session).create(data=theme_data, owner_id=owner_id, project_id=project_id)
        return new_theme
    
    async def update_theme(self, project_id: int, theme_id: int, theme_data: ThemeUpdate):
        upd_theme = await ThemeRepository(self.session).update(theme_id, theme_data)
        return upd_theme
    
    async def delete_theme(self, project_id: int, theme_id: int):
        await ThemeRepository(self.session).delete(theme_id)