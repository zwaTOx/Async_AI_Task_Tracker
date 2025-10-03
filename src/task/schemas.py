from datetime import datetime
from typing import Literal, Optional
from src.models import CustomBase

class TaskCreate(CustomBase):
    title: str
    description: Optional[str]
    color: str
    status: Optional[Literal["Назначена", "В работе", "Выполенена"]] = "Назначена"
    
    performer_id: Optional[int] = None

class TaskResponse(CustomBase):
    id: int
    title: str
    description: Optional[str]
    color: str
    status: str
    start: Optional[datetime]
    end: Optional[datetime]
    creator_id: int
    performer_id: Optional[int]
    project_id: int

class TaskPagination(CustomBase):
    items: list[TaskResponse]