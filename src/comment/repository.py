from src.repository import SQLAlchemyRepository
from .model import Comment
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from .schemes import PaginationParams

class CommentRepository(SQLAlchemyRepository):
    model = Comment
    async def get_with_creator(self, comment_id: int):
        query = select(Comment).where(Comment.id == comment_id)
        query = query.options(selectinload(Comment.creator))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, task_id: int, pagination: PaginationParams):
        statement = (
        select(Comment)
        .where(Comment.task_id == task_id)
        .options(
            selectinload(Comment.creator),
            selectinload(Comment.parent_comment).selectinload(Comment.creator)
        )
        .order_by(Comment.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
        result = await self.session.exec(statement)
        return result.scalars().all()