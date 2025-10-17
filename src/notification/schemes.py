from datetime import datetime
from typing import Optional
from pydantic import Field

from src.schemas import CustomBase
from src.config import settings

MESSAGE_FIELD = Field(max_length=100)

class NotificationCreate(CustomBase):
    message: str = MESSAGE_FIELD
    user_id: int
    link: Optional[str] = None

class ProjectNotificationCreate(CustomBase):
    message: str = MESSAGE_FIELD
    link: Optional[str] = None

class NotificationResponse(CustomBase):
    id: int
    user_id: int
    message: str = MESSAGE_FIELD
    link: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class NotificationPargination(CustomBase):
    notifications: list[NotificationResponse]
    limit: int = settings.NOTIF_DEFAULT_LIMIT
