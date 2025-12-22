from datetime import datetime
from typing import Literal, Optional

from pydantic import Field
from src.attachment.schemes import AttachResponse
from src.schemas import CustomBase, TimeStampSchema
from src.subtask.schemas import SubtaskResponse
from src.tag.schemes import TagResponse
from src.user.schemes import UserTaskResponse 

class TaskBase(CustomBase):
    id: int
    title: str
    description: Optional[str] = None
    color: str
    status: str
    priority: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    creator_id: int
    performer_id: Optional[int] = None
    project_id: int

class TaskCreate(CustomBase):
    title: str
    description: Optional[str]
    color: str
    priority: Optional[Literal["Низкий", "Средний", "Высокий", "Критический"]] = Field(default=None)
    status: Optional[Literal["Назначена", "В работе", "Выполнена"]] = Field(default="Назначена")
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    performer_id: Optional[int] = Field(default=None)

class TaskResponse(TimeStampSchema, TaskBase):
    pass

class TaskResponseWithSubtasks(TaskResponse):
    tags: list[TagResponse]
    subtasks: list[SubtaskResponse]
    creator: UserTaskResponse
    performer: Optional[UserTaskResponse]
    attachments: list[AttachResponse]
    
class TaskPagination(CustomBase):
    items: list[TaskResponse]

class TaskUpdate(CustomBase):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    color: Optional[str] = Field(default=None)
    priority: Optional[Literal["Низкий", "Средний", "Высокий", "Критический"]] = Field(default=None)
    status: Optional[Literal["Назначена", "В работе", "Выполнена"]] = Field(default=None)
    tags: Optional[list[int]] = Field(default=None)
    files: Optional[list[int]] = Field(default=None)
    
    performer_id: Optional[int] = Field(default=None, description="ID исполнителя. Если передать 0, исполнитель будет сброшен")