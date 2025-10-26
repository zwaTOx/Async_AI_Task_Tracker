from typing import Any, Dict
from src.repository import SQLAlchemyRepository
from .model import Comment
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select

class CommentRepository(SQLAlchemyRepository):
    model = Comment
    async def get_all(self, **filters: Dict[str, Any]):
        query = select(self.model).options(selectinload(Comment.replies))
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
        result = await self.session.execute(query)
        return result.scalars().all()