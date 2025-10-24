from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Comment(Base):
    id: Mapped[int_pk]
    text: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
