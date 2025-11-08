from sqlalchemy import ForeignKey, Text
from src.database import Base, int_pk
from sqlalchemy.ext.hybrid import hybrid_property
from src.models import TimeStampMixin
from src.vote.models import Vote
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Idea(Base, TimeStampMixin):
    id: Mapped[int_pk]
    text: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    votes: Mapped[list["Vote"]] = relationship('Vote', backref='idea', cascade="all, delete-orphan")
    
    @hybrid_property
    def votes_count(self) -> int:
        return len(self.votes) if self.votes else 0