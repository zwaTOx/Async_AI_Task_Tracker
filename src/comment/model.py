from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import ForeignKey
from src.models import TimeStampMixin

class Comment(Base, TimeStampMixin):
    id: Mapped[int_pk]
    text: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), 
        nullable=True
    )
    replies: Mapped[list["Comment"]] = relationship(
        "Comment",
        backref=backref("parent", remote_side="Comment.id")
    )
    # task: Mapped["Task"] = relationship("Task", back_populates="comments")

    @property
    def replies_count(self) -> int:
        return len(self.replies) if self.replies else 0