from typing import Literal
from sqlalchemy import ForeignKey, String
from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Task(Base):
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[Literal["Назначена", "В работе", "Выполенена"]] = mapped_column(default="Назначена")
    start: Mapped[datetime] = mapped_column(nullable=True)
    end: Mapped[datetime] = mapped_column(nullable=True)
    #Время обновления
    #Время создания

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    performer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    #tags
    #file_id

    