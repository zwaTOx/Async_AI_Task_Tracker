from sqlmodel.ext.asyncio.session import AsyncSession

class InviteCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

