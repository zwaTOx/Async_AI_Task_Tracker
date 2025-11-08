from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.database import DbSession
from .dependencies import WSCurrentUser
from .manager import ws_manager

ws_router = APIRouter()

@ws_router.websocket("/ws/connect/")
async def connect_to_ws(
    websocket: WebSocket, 
    session :DbSession,
    user: WSCurrentUser
):
    await ws_manager.connect(websocket, user.id)
    try:
        await ws_manager.send_personal_message(user.id, {"type": "welcome", "user_id": user.id})
        while True:
            data = await websocket.receive_json()
            await ws_manager.send_personal_message(user.id, {"type": "echo", "payload": data})

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, user.id)