

from typing import Annotated
from fastapi import Depends, WebSocket
from src.config import settings
from src.database import DbSession
from src.exceptions import AuthException
from jose import JWTError, jwt
from src.user.models import User
from src.user.repository import UserRepository


async def get_ws_user(
    websocket: WebSocket,
    session: DbSession
):
    token = websocket.query_params.get("token")
    if not token:
        token = websocket.headers.get("Authorization")
        # if authorization and authorization.startswith("Bearer "):
        #     token = authorization[7:]
    if not token:
        raise AuthException(detail="Token required")
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.USER_JWT_ALG]
        )
        user_id = payload.get('sub')
    except JWTError:
        raise AuthException(detail="Could not validate user")
    
    if not user_id:
        raise AuthException(detail="Invalid token payload")
    
    user = await UserRepository(session).get_by_id(user_id=int(user_id))
    if not user:
        raise AuthException(detail="User not found")
    
    return user

WSCurrentUser = Annotated[User, Depends(get_ws_user)]