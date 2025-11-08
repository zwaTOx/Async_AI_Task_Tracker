from typing import Any, Dict
from src.repository import SQLAlchemyRepository
from .model import Comment
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select

class CommentRepository(SQLAlchemyRepository):
    model = Comment
    async def get_all(self, task_id: int):
        statement = (
        select(Comment)
        .where(Comment.task_id == task_id)
        .options(
            selectinload(Comment.creator),
            selectinload(Comment.parent_comment).selectinload(Comment.creator)
        )
        .order_by(Comment.created_at)
    )
    
        result = await self.session.exec(statement)
        return result.scalars().all()