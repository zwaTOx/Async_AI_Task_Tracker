from src.models import CustomBase

class UserResponse(CustomBase):
    id: int
    email: str

class UserCreate(CustomBase):
    email: str
    password: str
    verify_password: str

class UserLogin(CustomBase):
    email: str
    password: str

class ResetPasswordData(CustomBase):
    password: str
