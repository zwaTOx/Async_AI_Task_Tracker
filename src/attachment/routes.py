from fastapi import APIRouter, Depends, File, status, UploadFile, Response
from fastapi.responses import FileResponse

from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_member
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
    response: Response,
    user: CurrentUser,
    user_id: int
):
    file_path = await AttachmentService(session).get_user_icon_file(user_id)
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    return FileResponse(file_path)

@attach_router.get(
    "/projects/{project_id}/icon",
    dependencies=[Depends(verify_project_member)]
)
async def get_project_icon(
    session: DbSession,
    user: CurrentUser,
    response: Response,
    project_id: int
):
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    file_path = await AttachmentService(session).get_project_icon_file(project_id)
    return FileResponse(file_path)