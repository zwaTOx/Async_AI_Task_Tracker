from fastapi import APIRouter, status

from src.database import DbSession
from .service import CodeService

code_router = APIRouter()

@code_router.post(
    "/forgot-password",
    status_code=status.HTTP_201_CREATED
)
async def send_reset_code(
    session: DbSession,
    email: str
):
    code, user_id = await CodeService(session).reset_password(email)
    return {
        "dev_info": code,
        "user_id": user_id
    }


@code_router.post(
    "/reset-code",
    status_code=status.HTTP_201_CREATED
)
async def create_reset_password_token(
    session: DbSession,
    user_id: int,
    code: str
):
    token = await CodeService(session).get_token_from_code(user_id, code)
    return {
        "token": token
    }
