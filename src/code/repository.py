from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Code

class CodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_restore_code(self, user_id: int, code: str) -> str:
        new_user = Code(
            code=code,
            user_id=user_id
        )
        self.session.add(new_user)
        await self.session.commit()
        return code
    