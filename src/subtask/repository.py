from sqlalchemy.ext.asyncio.session import AsyncSession
from src.repository import SQLAlchemyRepository
from .models import Subtask


class SubtaskRepository(SQLAlchemyRepository):
    model = Subtask