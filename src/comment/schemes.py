from src.schemas import CustomBase

class CommentBase(CustomBase):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    owner_id: int
    task_id: int

class CommentPargination(CustomBase):
    items: list[CommentResponse]