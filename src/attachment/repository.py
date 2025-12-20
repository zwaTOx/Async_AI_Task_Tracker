from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .model import Attachment, AttachmentType

class AttachmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_file(self, system_filename: str, user_filename: str, user_id: int, attach_type: AttachmentType):
        attach = Attachment(
            system_filename=system_filename,
            user_filename = user_filename,
            user_id=user_id,
            attach_type=attach_type
        )
        self.session.add(attach)
        await self.session.commit()
        return attach
    
    async def get_attachment_by_id(self, attach_id: int):
        statement = select(Attachment).filter(Attachment.id==attach_id)
        result = await self.session.exec(statement)
        return result.first()