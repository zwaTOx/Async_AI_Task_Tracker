from typing import Annotated
from fastapi import Depends, Request
from jose import JWTError, jwt
from src.exceptions import AuthException
from src.config import settings
from src.user.repository import User

def get_current_user(
    request: Request
) -> str:
    token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.USER_JWT_ALG])
        user_id = payload.get('sub')
    except JWTError:
        raise AuthException(detail="Could not validate user")
    if not user_id:
        raise AuthException(detail="Invalid token payload")
    user = User(request.state.db).get_by_id(
        user_id=user_id
    )
    if not user:
        raise AuthException(detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]