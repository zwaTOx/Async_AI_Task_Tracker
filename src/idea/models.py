from sqlalchemy import ForeignKey, Text
from src.database import Base, int_pk
from src.models import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column

class Idea(Base, TimeStampMixin):
    id: Mapped[int_pk]
    text: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))