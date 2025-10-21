import json
from typing import List
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.repository import SQLAlchemyRepository
from src.config import settings
from .schemes import ProjectNotificationCreate, NotificationResponse
from .model import Notification

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            existing_connection = self.active_connections[user_id]
            try:
                await existing_connection.close()
            except Exception as e:
                pass
            finally:
                del self.active_connections[user_id]
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, payload: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(payload)

    async def broadcast_to_all(self, message: dict):
        disconnected_users = []
        
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected_users.append(user_id)
        
        for user_id in disconnected_users:
            if user_id in self.active_connections:
                del self.active_connections[user_id]

manager = ConnectionManager()

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