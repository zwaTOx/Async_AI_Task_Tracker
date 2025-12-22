from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.repository import SQLAlchemyRepository
from .model import Attachment, AttachmentType, attachment_task

class AttachmentRepository(SQLAlchemyRepository):
    model = Attachment

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
    
    async def get_task_file(self, task_id: int, file_id: int) -> Optional[Attachment]:
        statement = select(Attachment).join(
            attachment_task, 
            Attachment.id == attachment_task.c.attachment_id
        ).where(
            (attachment_task.c.task_id == task_id) &
            (Attachment.id == file_id)
        )
        
        result = await self.session.exec(statement)
        return result.scalar_one_or_none()
    
    async def   unpin_file(self, task_id: int, file_id: int):
        statement = delete(attachment_task).where(
            (attachment_task.c.task_id == task_id) &
            (attachment_task.c.attachment_id == file_id)
        )
        
        result = await self.session.execute(statement)
        await self.session.commit()