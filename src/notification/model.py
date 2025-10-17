from sqlalchemy.orm import Mapped, mapped_column 

from src.database import Base, int_pk
from src.models import TimeStampMixin


class Notification(Base, TimeStampMixin):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
