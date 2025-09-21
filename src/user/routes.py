from fastapi import APIRouter, Response, status

from src.database import DbSession
from .schemes import UserLogin, UserResponse, UserCreate
from .service import UserService

user_router = APIRouter()

@user_router.post(
    "/register",
    response_model=UserResponse,
)
async def create_user(
    session: DbSession,
    user_create_data: UserCreate
):
    """Creates a new user."""
    new_user = await UserService(session).register_user(user_create_data)
    return new_user

@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def auth_user(
    session: DbSession,
    user_login_data: UserLogin,
    response: Response
):
    token = await UserService(session).auth_user(user_login_data)
    response.set_cookie(
        key='access_token',
        value=token, 
        httponly=True,
        secure=True
    )
    return {
        "message": "HttpOnly cookie set successfully"
    }