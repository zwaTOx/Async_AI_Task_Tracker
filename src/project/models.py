
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, int_pk


class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))