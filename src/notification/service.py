from typing import Dict, List
import logging
from fastapi import WebSocket

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
