from fastapi import APIRouter, File, status, UploadFile

from src.user.dependencies import CurrentUser
from src.database import DbSession
from .service import AttachmentService

attach_router = APIRouter()

@attach_router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def upload_attachment(
    session: DbSession,
    user: CurrentUser,
    attachment: UploadFile = File(...)
):
    new_attach = await AttachmentService(session).upload_file(attachment, user.id)
    return new_attach
    