from src.repository import SQLAlchemyRepository
from .model import Tag

class TagRepository(SQLAlchemyRepository):
    model = Tag