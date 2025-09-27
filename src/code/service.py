from sqlmodel.ext.asyncio.session import AsyncSession

from src.code.repository import CodeRepository
from src.email.password import send_recovery_code
from src.exceptions import BadRequestException
from src.user.repository import UserRepository
from .utils import create_reset_password_token, decode_reset_password_token

class CodeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def reset_password(self, email: str):
        founded_user = await UserRepository(self.session).get_user_by_email(email)
        if founded_user is None:
            raise BadRequestException("Пользователя с таким email не существует")
        code = send_recovery_code(email)
        await CodeRepository(self.session).create_restore_code(founded_user.id, code)
        return code, founded_user.id
    
    async def get_token_from_code(self, user_id: int, code: str):
        code = await CodeRepository(self.session).get_code(user_id, code)
        if code is None or code.is_used:
            raise BadRequestException("Неверное введенный код")
        await CodeRepository(self.session).use_code(code.id)
        token = create_reset_password_token(user_id)
        return token