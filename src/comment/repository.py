from src.repository import SQLAlchemyRepository
from .model import Comment

class CommentRepository(SQLAlchemyRepository):
    model = Comment