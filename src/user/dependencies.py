from typing import Annotated
from fastapi import Depends, Request
from jose import JWTError, jwt
from src.exceptions import AuthException
from src.config import settings
from src.database import DbSession
from .repository import UserRepository
from .models import User

async def get_current_user(
    request: Request,
    session: DbSession
):
    authorization: str = request.headers.get("Authorization")
    if not authorization: 
        token = request.cookies.get("access_token")
        if not token:
            raise AuthException(detail="Token required")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.USER_JWT_ALG])
        user_id = payload.get('sub')
    except JWTError:
        raise AuthException(detail="Could not validate user")
    if not user_id:
        raise AuthException(detail="Invalid token payload")
    user = await UserRepository(session).get_by_id(
        user_id=int(user_id)
    )
    if not user:
        raise AuthException(detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]