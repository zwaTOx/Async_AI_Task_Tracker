from typing import Optional, Annotated

from pydantic import AfterValidator, EmailStr
from sqlmodel import Field
from src.schemas import CustomBase


def validate_username_starts(value: Optional[str]) -> Optional[str]:
    if value is not None and not value.startswith('@'):
        raise ValueError('Имя пользователя должно начинаться с @')
    return value

USERNAME_FIELD = Field(None, min_length=5, max_length=50, description="Имя пользователя должно начинаться с '@'")
BIO_FIELD = Field(None, max_length=300)
NICKNAME_FIELD = Field(None, max_length=50)

UsernameType = Annotated[Optional[str], AfterValidator(validate_username_starts), USERNAME_FIELD]

class UserResponse(CustomBase):
    id: int
    email: str
    username: UsernameType = USERNAME_FIELD
    nickname: Optional[str] = NICKNAME_FIELD
    bio: str = BIO_FIELD
    icon_id: int | None

class UserCreate(CustomBase):
    email: str
    username: Optional[UsernameType] = USERNAME_FIELD
    password: str
    verify_password: str

class UserLogin(CustomBase):
    login: EmailStr | UsernameType
    password: str

class UserUpdateData(CustomBase):
    username: Optional[UsernameType] = USERNAME_FIELD
    nickname: Optional[str] = NICKNAME_FIELD
    icon_id: Optional[int] = None
    bio: Optional[str] = BIO_FIELD

class ResetPasswordData(CustomBase):
    password: str
