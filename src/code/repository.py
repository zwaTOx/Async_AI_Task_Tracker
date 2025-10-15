from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.code.schemes import CodeResponse
from .models import Code

class CodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_code(self, user_id: int, code: str) -> int:
        new_code = Code(
            code=code,
            user_id=user_id
        )
        self.session.add(new_code)
        await self.session.commit()
        return new_code.id
    
    async def get_code(self, user_id: int, code: int, code_type: str = "Restore"):
        statement = select(Code).filter(
            Code.user_id == user_id, Code.code==code, Code.code_type==code_type
        )
        result = await self.session.exec(statement)
        return result.scalars().first()
    
    async def use_code(self, code_id: int):
        statement = select(Code).filter(
            Code.id == code_id)
        result = await self.session.exec(statement)
        code = result.scalars().one_or_none()
        code.is_used = True
        self.session.add(code)
        await self.session.commit()
        return code