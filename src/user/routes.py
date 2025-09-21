from fastapi import APIRouter

from src.database import DbSession
from .schemes import UserResponse, UserCreate
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
