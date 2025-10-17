from datetime import datetime
from pydantic import Field

from src.schemas import CustomBase
from src.config import settings

MESSAGE_FIELD = Field(max_length=100)

class NotificationCreate(CustomBase):
    message: str = MESSAGE_FIELD
    user_id: int

class ProjectNotificationCreate(CustomBase):
    message: str = MESSAGE_FIELD

class NotificationResponse(CustomBase):
    id: int
    user_id: int
    message: str = MESSAGE_FIELD
    created_at: datetime
    updated_at: datetime

class NotificationPargination(CustomBase):
    notifications: list[NotificationResponse]
    limit: int = settings.NOTIF_DEFAULT_LIMIT
