from typing import TYPE_CHECKING
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, int_pk
from src.category.models import project_category


class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    categories = relationship(
        "Category", 
        secondary=project_category, 
        back_populates="projects"
    )