from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import ConflictException, InvalidPasswordException, AuthException, BadRequestException
from .schemes import UserCreate, UserResponse, UserLogin
from src.email.password import send_recovery_code
from src.code.repository import CodeRepository
from .repository import UserRepository
from .utils import verify_password, generate_auth_token

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def find_one_or_one()

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
    
    async def auth_user(self, user_auth_data: UserLogin):
        founded_user = await UserRepository(self.session).get_user_by_email(
            user_auth_data.email
        )
        if founded_user is None:
            raise AuthException
        if not verify_password(user_auth_data.password, founded_user.hashed_password):
            raise AuthException
        return generate_auth_token(founded_user.id), founded_user.id
    
    async def reset_password(self, email: str):
        founded_user = await UserRepository(self.session).get_user_by_email(email)
        if founded_user is None:
            raise BadRequestException("Пользователя с таким email не существует")
        code = send_recovery_code(email)
        await CodeRepository(self.session).create_restore_code(founded_user.id, code)
        