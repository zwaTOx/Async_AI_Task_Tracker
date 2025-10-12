from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, int_pk


class Subtask(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    complited: Mapped[bool] = False
    task_id: Mapped[int] = mapped_column(foreign_key="tasks.id")