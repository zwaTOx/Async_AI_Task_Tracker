from datetime import datetime, timedelta, timezone
from random import randint
from jose import JWTError, jwt
from src.config import settings
from src.exceptions import AuthException
from src.user_project_association.schemes import InviteProjectData

def create_invite_project_token(project_id: int, user_id: int, role: str):
    encode = {'project_id': project_id, 'user_id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + timedelta(hours=settings.INVITE_CODE_EXCPIRES_HOURS)
    encode.update({'exp': expires})
    return jwt.encode(
        encode, settings.INVITE_CODE_SECRET_KEY, algorithm=settings.INVITE_CODE_SECRET_ALG
    )

def decode_invite_project_token(invite_token: str) -> InviteProjectData:
    try:
        payload = jwt.decode(invite_token, 
            settings.INVITE_CODE_SECRET_KEY, algorithms=[settings.INVITE_CODE_SECRET_ALG])
        current_time = datetime.now(timezone.utc)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            if current_time > exp_datetime:
                raise AuthException("Токен приглашения истек")
        return InviteProjectData(**payload)
    except JWTError as e:
            if isinstance(e, jwt.ExpiredSignatureError):
                raise AuthException("Токен приглашения истек")
            else:
                raise AuthException("Недопустимый токен приглашения")
            
def create_reset_password_token(user_id: int):
    encode = {'user_id': user_id}
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.RESET_CODE_EXCPIRES_MINUTES)
    encode.update({'exp': expires})
    return jwt.encode(
        encode, settings.RESET_CODE_SECRET_KEY, algorithm=settings.RESET_CODE_SECRET_ALG
    )

def decode_reset_password_token(token: str) -> int:
    try:
        payload = jwt.decode(token, 
            settings.RESET_CODE_SECRET_KEY, algorithms=[settings.RESET_CODE_SECRET_ALG])
        current_time = datetime.now(timezone.utc)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            if current_time > exp_datetime:
                raise AuthException("Токен смены пароля истек")
        return payload['user_id']
    except JWTError as e:
        if isinstance(e, jwt.ExpiredSignatureError):
            raise AuthException("Токен восстановления пароля истек")
        else:
            raise AuthException("Недопустимый токен восстановления пароля")
        
def generate_code() -> str:
    code = f'{randint(0, 999999):06}'
    return code