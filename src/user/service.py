from sqlmodel.ext.asyncio.session import AsyncSession
from src.attachment.repository import AttachmentRepository
from src.exceptions import ConflictException, InvalidPasswordException, AuthException, BadRequestException, NotFoundException
from src.code.utils import decode_reset_password_token
from .schemes import UserCreate, UserResponse, UserLogin, ResetPasswordData, UserUpdateData
from .repository import UserRepository
from .utils import verify_password, generate_auth_token, generate_username

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
            raise ConflictException("Пользователь с таким email уже существует")
        if user_create_data.username is None:
            username = await generate_username(user_create_data.email)
            user_create_data.username = username
        elif user_create_data.username is not None:
            user_with_same_username = await UserRepository(self.session).get_user_by_username(user_create_data.username)
            if user_with_same_username is not None:
                raise ConflictException("Пользователь с таким username уже существует")
        new_user = await UserRepository(self.session).create_user(user_create_data)
        return new_user
    
    async def auth_user(self, user_auth_data: UserLogin):
        if user_auth_data.login.startswith('@'):
            founded_user = await UserRepository(self.session).get_user_by_username(
                user_auth_data.login
            )
        else:
            founded_user = await UserRepository(self.session).get_user_by_email(
                user_auth_data.login
            )
        if founded_user is None:
            raise AuthException
        if not verify_password(user_auth_data.password, founded_user.hashed_password):
            raise AuthException
        return generate_auth_token(founded_user.id), founded_user.id
    
    async def update_user(self, user_id: int, user_update_data: UserUpdateData):
        if user_update_data.icon_id is not None:
            attach = await AttachmentRepository(self.session).get_attachment_by_id(user_update_data.icon_id)
            if attach is None:
                raise NotFoundException("Вложение не найдено")
        if user_update_data.username is not None:
            user_with_same_username = await UserRepository(self.session).get_user_by_username(user_update_data.username)
            if user_with_same_username is not None:
                raise ConflictException("Пользователь с таким username уже существует")
        upd_user = await UserRepository(self.session).update_user_info(user_id, user_update_data)
        return upd_user

    async def reset_password(self, token: str, password_update_data: ResetPasswordData):
        user_id = decode_reset_password_token(token)
        user = await UserRepository(self.session).get_by_id(user_id)
        if verify_password(password_update_data.password, user.hashed_password):
            raise BadRequestException("Нельзя изменить пароль на старный пароль")
        await UserRepository(self.session).update_password(user_id, password_update_data)
        
        