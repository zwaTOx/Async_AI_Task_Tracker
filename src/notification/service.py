from typing import Dict, List
import logging
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession 

from .repository import NotificationRepository
from .schemes import NotificationCreate, NotificationResponse, ProjectNotificationCreate
from src.user_project_association.repository import UserProjectAssociationRepository

active_connections: Dict[int, List[WebSocket]] = {}


async def send_notification_to_user(user_id: int, payload: dict) -> int:
    """Send a JSON payload to all active websocket connections for a user.
    Returns number of successful sends.
    """
    logging.info('Начинаю отправку уведомления пользователю: %d с полезной нагрузкой: %s', user_id, payload)
    sent = 0
    conns = active_connections.get(user_id, []).copy()
    for ws in conns:
        try:
            await ws.send_json(payload)
            sent += 1
            logging.info("Отправил уведомление: пользователю: %d", user_id)
        except Exception:
            try:
                await ws.close()
            except Exception:
                pass
            if ws in active_connections.get(user_id, []):
                active_connections[user_id].remove(ws)
    if user_id in active_connections and not active_connections[user_id]:
        del active_connections[user_id]
    return sent


async def broadcast(payload: dict) -> int:
    """Send a payload to all connected users. Returns number of successful sends."""
    sent = 0
    for user_id in list(active_connections.keys()):
        sent += await send_notification_to_user(user_id, payload)
    return sent


async def remove_websocket(user_id: int, websocket: WebSocket) -> None:
    conns = active_connections.get(user_id, [])
    if websocket in conns:
        try:
            await websocket.close()
        except Exception:
            pass
        conns.remove(websocket)
    if not conns and user_id in active_connections:
        del active_connections[user_id]


async def disconnect_user(user_id: int) -> None:
    conns = active_connections.pop(user_id, [])
    for ws in conns:
        try:
            await ws.close()
        except Exception:
            pass

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