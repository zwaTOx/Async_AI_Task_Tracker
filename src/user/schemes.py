from typing import Optional

from sqlmodel import Field
from src.models import CustomBase

class UserResponse(CustomBase):
    id: int
    email: str
    username: str
    bio: str
    icon_id: int|None

class UserCreate(CustomBase):
    email: str
    password: str
    verify_password: str

class UserLogin(CustomBase):
    email: str
    password: str

class UserUpdateData(CustomBase):
    username: Optional[str] = Field(None, min_length=5, max_length=50)
    icon_id: Optional[int] = Field(None)
    bio: Optional[str] = Field(None, min_length=1, max_length=300)

class ResetPasswordData(CustomBase):
    password: str
