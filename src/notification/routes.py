from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect, HTTPException, status

from src.database import DbSession
from .schemes import NotificationPargination, NotificationCreate, NotificationResponse, ProjectNotificationCreate
from .service import NotificationService
from .repository import manager, ConnectionManager
from src.user.dependencies import CurrentUser  
from src.user_project_association.dependencies import verify_project_member
from src.config import settings 

notification_router = APIRouter()

@notification_router.get(
    "/api/notifications",
    response_model=NotificationPargination,
)
async def get_notifications(
    session: DbSession,
    current_user: CurrentUser,
    limit: int = settings.NOTIF_DEFAULT_LIMIT
):
    notifications = await NotificationService(session).get_notifications(current_user.id, limit)
    return { 
        "notifications": notifications, 
        "limit": limit
    }

@notification_router.post(
    "/api/notifications",
    response_model=NotificationResponse
)
async def create_notification(
    session: DbSession,
    user: CurrentUser,
    notif_data: NotificationCreate
):
    new_notif = await NotificationService(session).create_notification(notif_data)
    return new_notif

@notification_router.websocket("/ws/{user_id}")
async def notifications_ws(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint for user notifications.
    Connects the socket to the ConnectionManager and keeps the connection alive.
    """
    await manager.connect(websocket)
    try:
        await manager.send_personal_message({"type": "welcome", "user_id": user_id}, websocket)
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message({"type": "echo", "payload": data}, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@notification_router.post(
    "/api/notifications/project/{project_id}",
    dependencies=[Depends(verify_project_member)]
)
async def create_project_notification(
    session: DbSession,
    user: CurrentUser,
    project_id: int,
    notif_data: ProjectNotificationCreate
):
    notifications = await NotificationService(session).create_project_notification(user.id, project_id, notif_data)
    try:
        await manager.send_personal_message(user.id, {
            "type": "project_notifications",
            "project_id": project_id,
            "notifications": notifications
        })
    except Exception:
        pass
    return {"notifications": notifications}