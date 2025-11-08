from typing import Literal
from src.database import Base, int_pk
from src.models import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Theme(Base, TimeStampMixin):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    max_voices: Mapped[int] = mapped_column(default=1)
    stage: Mapped[Literal["Brainshtorm", "Vote", "Finish"]] = mapped_column(default='Brainshtorm')

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))