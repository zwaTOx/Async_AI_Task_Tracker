from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException
from .repository import CommentRepository
from .schemes import CommentCreate, CommentResponse, CommentUpdate, PaginationParams

class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_comment(self, user_id: int, task_id: int, parent_comment_id: int|None, comment_data: CommentCreate) -> CommentResponse:
        if parent_comment_id:
            parent_comment = await CommentRepository(self.session).get(parent_comment_id)
            if not parent_comment or parent_comment.task_id != task_id:
                raise NotFoundException("Родительский комментарий не найден в задаче")
        new_comment = await CommentRepository(self.session).create(
            comment_data, owner_id=user_id, task_id=task_id, parent_comment_id=parent_comment_id
        )
        return new_comment
    
    async def get_comments(self, task_id: int, pagination: PaginationParams) -> CommentResponse:
        return await CommentRepository(self.session).get_all(task_id=task_id, pagination=pagination)
    
    async def update_comment(self, comment_id: int, comment_data: CommentUpdate) -> CommentResponse:
        upd_comment = await CommentRepository(self.session).update(comment_id, comment_data)
        return upd_comment
    
    async def delete_comment(self, comment_id: int):
        await CommentRepository(self.session).delete(comment_id)