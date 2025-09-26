from datetime import datetime, timedelta, timezone
from src.config import settings
from jose import jwt

def hash_password(password: str) -> str:
    #Обязательно сделать хеширование в проде
    hashed_password = password
    return hashed_password

def verify_password(password, hashed_password) -> bool:
    return password == hashed_password

def generate_auth_token(subject):
    """Generate a JWT token for the user."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.USER_JWT_EXP_MIN)
    
    data = {
        "exp": exp,  
        "sub": str(subject), 
    }
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.USER_JWT_ALG)