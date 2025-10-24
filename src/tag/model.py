from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

tag_task = Table(
    "tag_tasks",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    color: Mapped[str]
    description: Mapped[str]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    tasks = relationship("Task", secondary=tag_task, back_populates="tags")