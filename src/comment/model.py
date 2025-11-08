from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import ForeignKey
from src.models import TimeStampMixin

class Comment(Base, TimeStampMixin):
    id: Mapped[int_pk]
    text: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id', ondelete="CASCADE"))
    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="SET NULL"), 
        nullable=True
    )
    creator = relationship('User', foreign_keys=[owner_id], backref="created_comments")
    parent_comment = relationship(
        'Comment', 
        foreign_keys=[parent_comment_id],
        remote_side='Comment.id',  
        backref=backref('replies')
    )

    @property
    def replies_count(self) -> int:
        return len(self.replies) if self.replies else 0