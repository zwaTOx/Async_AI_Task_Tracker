from sqlalchemy import ForeignKey
from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Vote(Base):
    id: Mapped[int_pk]
    idea_id: Mapped[int] = mapped_column(ForeignKey("ideas.id"))
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))