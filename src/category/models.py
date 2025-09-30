from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, int_pk


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int_pk]
    name: Mapped[str]
    color: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))