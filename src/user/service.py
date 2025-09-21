from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import ConflictException, InvalidPasswordException
from .schemes import UserCreate, UserResponse
from .repository import UserRepository

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, user_create_data: UserCreate) -> UserResponse:
        if user_create_data.password != user_create_data.verify_password:
            raise InvalidPasswordException
        founded_user = await UserRepository(self.session).get_user_by_email(
            user_create_data.email
        )
        if founded_user is not None:
            raise ConflictException("User is already exists")
        new_user = await UserRepository(self.session).create_user(user_create_data)
        return new_user