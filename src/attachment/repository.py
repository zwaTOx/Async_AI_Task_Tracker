from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import Attachment

class AttachmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_icon(self, system_filename: str, user_filename: str, user_id):
        attach = Attachment(
            system_filename=system_filename,
            user_filename = user_filename,
            user_id=user_id
        )
        self.session.add(attach)
        await self.session.commit()
        return attach