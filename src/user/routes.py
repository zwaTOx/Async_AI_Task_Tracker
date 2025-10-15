from fastapi import APIRouter, Depends, Response, status

from src.database import DbSession
from .schemes import UserLogin, UserResponse, UserCreate, UserUpdateData, TokenResponse, ResetPasswordData, UpdatePasswordData
from .service import UserService
from .dependencies import CurrentUser

user_router = APIRouter()

@user_router.post(
    "/auth/sign-up",
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
    "/auth/sign-in",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def auth_user(
    session: DbSession,
    user_login_data: UserLogin,
    response: Response
):
    token, user_id = await UserService(session).auth_user(user_login_data)
    response.set_cookie(
        key='access_token',
        value=token, 
        httponly=True,
        samesite='none',
        secure=True
    )
    return {
        "access_token": token,
        "user_id": user_id
    }

@user_router.put(
    "/auth/reset-password",
)
async def reset_password(
    session: DbSession,
    token: str,
    password_update_data: ResetPasswordData
):
    await UserService(session).reset_password(token, password_update_data)
    return {
        "message": "Пароль успешно обновлен"
    }

@user_router.get(
    "/users/me",
    response_model=UserResponse
)
async def get_my_profile(
    session: DbSession,
    user: CurrentUser
):
    return user

@user_router.patch(
    "/users/me",
    response_model=UserResponse,
)
async def update_user(
    session: DbSession,
    user: CurrentUser,
    user_update_data: UserUpdateData
):
    upd_user = await UserService(session).update_user(user.id, user_update_data)
    return upd_user

@user_router.put(
    "/users/me/update-password"
)
async def update_password(
    session: DbSession,
    user: CurrentUser,
    upd_data: UpdatePasswordData
):
    await UserService(session).update_password(user.id, upd_data)
    return {"message": "Пароль успешно изменен"}