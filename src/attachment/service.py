import uuid
import os
from pathlib import Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import UploadFile

from src.config import settings
from src.exceptions import TooLargeEntityException, BadRequestException
from .repository import AttachmentRepository
from .schemes import AttachResponse

MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB

class AttachmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def upload_file(self, upload_file: UploadFile, user_id: int) -> AttachResponse:
        unique_filename = str(uuid.uuid4())
        file_extension = Path(upload_file.filename).suffix
        filename = unique_filename + file_extension
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
        contents = await upload_file.read()
        file_size = len(contents)
        if file_size > settings.MAX_FILE_SIZE_MB:
            raise TooLargeEntityException(f"Файл слишком большой. Максимальный размер: {settings.MAX_FILE_SIZE_MB // (1024 * 1024)} МБ")
        content_type = upload_file.content_type
        if content_type not in settings.ALLOWED_ICON_TYPES:
            raise BadRequestException("Недопустимый формат файла")
        with open(file_path, 'wb') as f:
            f.write(contents)
        new_attach = await AttachmentRepository(self.session).add_icon(filename, upload_file.filename, user_id)
        return new_attach