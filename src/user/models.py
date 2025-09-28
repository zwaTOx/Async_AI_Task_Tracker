from sqlalchemy import ForeignKey, String
from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), default="User")
    bio: Mapped[str] = mapped_column(String(), default="")
    icon_id: Mapped[int] = mapped_column(ForeignKey("attachments.id"), nullable=True)
