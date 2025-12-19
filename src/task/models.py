from typing import Literal
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.models import TimeStampMixin
from src.tag.model import tag_task
from src.database import Base, int_pk

class Task(Base, TimeStampMixin):
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[Literal["Назначена", "В работе", "Выполнена"]] = mapped_column(default="Назначена")
    priority: Mapped[Literal["Низкий", "Средний", "Высокий", "Критический"]] = mapped_column(None, nullable=True)
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    performer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    
    creator = relationship('User', foreign_keys=[creator_id], backref="created_tasks")
    performer = relationship('User', foreign_keys=[performer_id], backref="appointed_tasks")
    subtasks = relationship('Subtask', backref='parent_task', cascade="all, delete-orphan")
    tags = relationship('Tag', secondary=tag_task, back_populates="tasks")
    comments = relationship('Comment', backref='task', cascade="all, delete-orphan")
    #file_id

    