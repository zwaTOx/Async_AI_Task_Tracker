from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, int_pk

class InviteCode(Base):
    id: Mapped[int_pk]
    user_id = Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    code = Mapped[String(8)]= mapped_column(nullable=False, index=True)  
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())