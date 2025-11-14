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
    parent_comment_id: Optional[int]
    created_at: datetime
    updated_at: datetime
class CommentCreatorResponse(CommentResponse):
    creator: UserTaskResponse
    parent_comment: Optional[ParentCommentResponse]

class PaginationParams(CustomBase):
    skip: int = 0
    limit: int = 10

class CommentPargination(CustomBase):
    items: list[CommentCreatorResponse]
    params: PaginationParams