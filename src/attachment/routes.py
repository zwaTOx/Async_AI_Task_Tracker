from fastapi import APIRouter, File, status, UploadFile
from fastapi.responses import FileResponse

from src.user.dependencies import CurrentUser
from src.database import DbSession
from .service import AttachmentService

attach_router = APIRouter()

@attach_router.post(
    "/icons",
    status_code=status.HTTP_201_CREATED
)
async def upload_attachment(
    session: DbSession,
    user: CurrentUser,
    attachment: UploadFile = File(...)
):
    new_attach = await AttachmentService(session).upload_file(attachment, user.id)
    return new_attach
    
@attach_router.get(
    "/users/{user_id}/icon",
)
async def get_user_icon(
    session: DbSession,
    user: CurrentUser,
    user_id: int
):
    file_path = await AttachmentService(session).get_user_icon_file(user_id)
    return FileResponse(file_path)