from datetime import datetime
from typing import Literal
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, int_pk

class Code(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    code: Mapped[str]= mapped_column(nullable=False, index=True)  
    code_type: Mapped[Literal["Restore"]] = mapped_column(default="Restore")
    is_user: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())