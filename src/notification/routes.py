import asyncio
import json
from fastapi import BackgroundTasks, WebSocket, APIRouter, Depends, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from src.database import DbSession
from .schemes import NotificationPargination, NotificationCreate, NotificationResponse, ProjectNotificationCreate
from .service import NotificationService
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

# @notification_router.post(
#     "/api/notifications",
#     response_model=NotificationResponse
# )
# async def create_notification(
#     background_tasks: BackgroundTasks,
#     session: DbSession,
#     user: CurrentUser,
#     notif_data: NotificationCreate
# ):
#     new_notif = await NotificationService(session).create_notification(notif_data)
#     return new_notif

# @notification_router.post(
#     "/api/notifications/project/{project_id}",
#     dependencies=[Depends(verify_project_member)]
# )
# async def create_project_notification(
#     background_tasks: BackgroundTasks,
#     session: DbSession,
#     user: CurrentUser,
#     project_id: int,
#     notif_data: ProjectNotificationCreate
# ):
#     notifications = await NotificationService(session).create_project_notification(user.id, project_id, notif_data)
#     return {"notifications": notifications}