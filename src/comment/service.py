from sqlmodel.ext.asyncio.session import AsyncSession

from .repository import CommentRepository
from .schemes import CommentCreate, CommentResponse

class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_comment(self, user_id: int, task_id: int, comment_data: CommentCreate) -> CommentResponse:
        new_comment = await CommentRepository(self.session).create(comment_data, owner_id=user_id, task_id=task_id)
        return new_comment
    
    async def get_comments(self, task_id: int) -> CommentResponse:
        comments = await CommentRepository(self.session).get_all(task_id=task_id)
        return comments