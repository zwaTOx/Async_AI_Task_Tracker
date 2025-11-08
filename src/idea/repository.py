from src.repository import SQLAlchemyRepository
from .models import Idea

class IdeaRepository(SQLAlchemyRepository):
    model=Idea