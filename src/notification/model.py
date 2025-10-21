from sqlalchemy.orm import Mapped, mapped_column 

from src.database import Base, int_pk
from src.models import TimeStampMixin
from .schemes import NotificationResponse


class Notification(Base, TimeStampMixin):
    model = NotificationResponse
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=True)

    def to_read_model(self) -> NotificationResponse:
        return NotificationResponse(
            id=self.id,
            user_id=self.user_id,
            message=self.message,
            link=self.link,
        )