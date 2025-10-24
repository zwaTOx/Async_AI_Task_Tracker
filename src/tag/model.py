from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    color: Mapped[str]
    description: Mapped[str]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))