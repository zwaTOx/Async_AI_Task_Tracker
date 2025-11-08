from sqlalchemy import ForeignKey, String
from src.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column,relationship

class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=True)
    bio: Mapped[str] = mapped_column(String(), default="")
    icon_id: Mapped[int] = mapped_column(ForeignKey("attachments.id"), nullable=True)

    # created_tasks = relationship("Task", foreign_keys="Task.creator_id", back_populates="creator")
    projects = relationship("Project", secondary="userprojectassociations", back_populates="members")