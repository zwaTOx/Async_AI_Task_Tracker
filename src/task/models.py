from typing import Literal
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.models import TimeStampMixin
from src.database import Base, int_pk

class Task(Base, TimeStampMixin):
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[Literal["Назначена", "В работе", "Выполенена"]] = mapped_column(default="Назначена")
    start: Mapped[datetime] = mapped_column(nullable=True)
    end: Mapped[datetime] = mapped_column(nullable=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    performer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    #tags
    #file_id

    