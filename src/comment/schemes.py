from typing import Optional
from src.schemas import CustomBase
from datetime import datetime
from src.user.schemes import UserTaskResponse

class CommentBase(CustomBase):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class ParentCommentResponse(CommentBase):
    creator: UserTaskResponse

class CommentResponse(CommentBase):
    id: int
    owner_id: int
    task_id: int
    parent_comment_id: Optional[int] = None
    creator: UserTaskResponse
    parent_comment: Optional[ParentCommentResponse]
    created_at: datetime
    updated_at: datetime

class CommentPargination(CustomBase):
    items: list[CommentResponse]