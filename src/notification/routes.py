from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect, HTTPException, status

from src.database import DbSession
# from .schemes import NotificationResponse
from .service import active_connections
from src.user.dependencies import CurrentUser  
from . import service

notification_router = APIRouter()

@notification_router.get(
    "/websocket-info",
    summary="Информация о WebSocket соединении",
    response_description="Параметры WebSocket подключения"
)
async def get_websocket_info(current_user: CurrentUser):
    return {
        "ws_path": "/api/ws/notifications",
        "description": "Используйте этот путь для подключения к WebSocket для получения уведомлений в реальном времени.",
        "note": "фронтендер пiдоras"
    }

@notification_router.websocket("/ws/notifications")
async def ws_notifications(
    websocket: WebSocket,
    session: DbSession,
    current_user: CurrentUser
):
    await websocket.accept()
    user_id = current_user.id
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await service.remove_websocket(user_id, websocket)

@notification_router.post("/connect")
async def connect_user(
    session: DbSession,
    current_user: CurrentUser
):
    """
    HTTP-эндпоинт для "подключения" пользователя к системе.
    Используется для пометки пользователя как онлайн.
    """
    user_id = current_user.id
    if user_id not in active_connections:
        active_connections[user_id] = []
    return {
        "status": "connected",
        "user_id": user_id,
        "ws_path": "/ws/notifications"
    }

@notification_router.post("/disconnect")
async def disconnect_user(
    session: DbSession,
    current_user: CurrentUser
):
    user_id = current_user.id
    await service.disconnect_user(user_id)
    return {"status": "disconnected", "user_id": user_id}