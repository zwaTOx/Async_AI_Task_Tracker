from datetime import datetime
from typing import Literal, Optional

from pydantic import Field
from src.schemas import CustomBase, TimeStampSchema

class TaskBase(CustomBase):
    id: int
    title: str
    description: Optional[str] = None
    color: str
    status: str
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    creator_id: int
    performer_id: Optional[int] = None
    project_id: int

class TaskCreate(CustomBase):
    title: str
    description: Optional[str]
    color: str
    status: Optional[Literal["Назначена", "В работе", "Выполенена"]] = Field(default="Назначена")
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    performer_id: Optional[int] = Field(default=None)

class TaskResponse(TimeStampSchema, TaskBase):
    pass

class TaskPagination(CustomBase):
    items: list[TaskResponse]

class TaskUpdate(CustomBase):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    color: Optional[str] = Field(default=None)
    status: Optional[Literal["Назначена", "В работе", "Выполенена"]] = Field(default=None)
    
    performer_id: Optional[int] = Field(default=None, description="ID исполнителя. Если передать 0, исполнитель будет сброшен")