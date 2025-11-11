from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, int_pk


class Subtask(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))