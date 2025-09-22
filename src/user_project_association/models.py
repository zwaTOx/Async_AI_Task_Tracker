from sqlalchemy import DateTime, ForeignKey, func, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, int_pk
from .utils import Role

class UserProjectAssociation(Base):
    id: Mapped[int_pk]
    role: Mapped[str] = mapped_column(
        Enum(
            "OWNER", "ADMINISTRATOR", "READER", "USER", "INVITED",
            name="user_role_enum"
        ),
        nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    invited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

