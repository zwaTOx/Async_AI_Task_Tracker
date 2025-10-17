from sqlalchemy.ext.asyncio.session import AsyncSession
from .models import Theme
from src.repository import SQLAlchemyRepository

class ThemeRepository(SQLAlchemyRepository):
    model = Theme