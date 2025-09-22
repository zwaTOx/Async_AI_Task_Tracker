from datetime import datetime, timedelta
from jose import jwt
from src.config import settings

def create_invite_project_token(project_id: int, id: int):
    encode = {'project_id': project_id, 'id': id}
    expires = datetime.now() + timedelta(hours=settings.INVITE_CODE_EXCPIRES_HOURS)
    encode.update({'exp': expires})
    return jwt.encode(
        encode, settings.INVITE_CODE_SECRET_KEY, algorithm=settings.INVITE_CODE_SECRET_ALG
    )