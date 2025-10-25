from typing import Optional
from src.schemas import CustomBase

class SubtaskCreate(CustomBase):
    name: str
    completed: bool = False

class SubtaskResponse(CustomBase):
    id: int
    name: str
    completed: bool
    task_id: int

class SubtaskPargination(CustomBase):
    items: list[SubtaskResponse]

class SubtaskUpdate(CustomBase):
    name: Optional[str] = None
    completed: Optional[bool] = None