from typing import Dict, List
import logging
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession 

from .repository import NotificationRepository
from .schemes import NotificationCreate, NotificationResponse, ProjectNotificationCreate
from src.user_project_association.repository import UserProjectAssociationRepository

class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_notifications(self, user_id: int, limit: int) -> List[NotificationResponse]:
        notifications = await NotificationRepository(self.session).get_user_notifications(user_id, limit)
        return notifications
    
    async def create_notification(self, notif_data: NotificationCreate) -> NotificationResponse:
        new_notif = await NotificationRepository(self.session).create(notif_data)
        return NotificationResponse.model_validate(new_notif)
    
    async def create_project_notification(self, user_id: int, project_id: int, notif_data: ProjectNotificationCreate) -> List[NotificationResponse]:
        members = await UserProjectAssociationRepository(self.session).get_project_memberships(project_id)
        users_ids = [member.user_id for member in members] #if member.user_id != user_id
        notifications = await NotificationRepository(self.session).create_notifications(users_ids, notif_data)
        return notifications