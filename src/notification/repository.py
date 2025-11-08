from typing import List
from sqlalchemy import select, desc

from src.repository import SQLAlchemyRepository
from src.config import settings
from .schemes import ProjectNotificationCreate, NotificationResponse
from .model import Notification

class NotificationRepository(SQLAlchemyRepository):
    model = Notification
    
    async def get_user_notifications(self, user_id: int, limit: int = settings.NOTIF_DEFAULT_LIMIT):
        statement = select(Notification).where(Notification.user_id == user_id).order_by(desc(Notification.created_at)).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def create_notifications(self, 
        users_ids: List[int], 
        notif_data: ProjectNotificationCreate
    ) -> List[NotificationResponse]:
        notifications = []
        for user_id in users_ids:
            notifications.append(
                Notification(
                **notif_data.model_dump(exclude_none=True),
                user_id=user_id
                )
            ) 
        self.session.add_all(notifications)
        await self.session.commit()
        return notifications