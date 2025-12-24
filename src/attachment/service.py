import uuid
import os
from pathlib import Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import UploadFile

from src.attachment.model import AttachmentType
from src.user.repository import UserRepository
from src.project.repository import ProjectRepository
from src.config import settings
from src.exceptions import TooLargeEntityException, BadRequestException, NotFoundException
from .repository import AttachmentRepository
from .schemes import AttachResponse

MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB

class AttachmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def upload_icon(self, upload_file: UploadFile, user_id: int) -> AttachResponse:
        return await self._upload_file(
            upload_file=upload_file,
            user_id=user_id,
            allowed_types=settings.ALLOWED_ICON_TYPES,
            attachment_type="Attach"
        )

    async def upload_file(self, upload_file: UploadFile, user_id: int) -> AttachResponse:
        return await self._upload_file(
            upload_file=upload_file,
            user_id=user_id,
            allowed_types=settings.ALLOWED_FILE_TYPES,
            attachment_type="Attach"
        )

    async def _upload_file(
        self, 
        upload_file: UploadFile, 
        user_id: int, 
        allowed_types: list[str],
        attachment_type: AttachmentType
    ) -> AttachResponse:
        unique_filename = str(uuid.uuid4())
        file_extension = Path(upload_file.filename).suffix
        system_filename = f"{unique_filename}{file_extension}"
        contents = await upload_file.read()
        file_size = len(contents)
        if file_size > settings.MAX_FILE_SIZE_MB:
            raise TooLargeEntityException(
                f"Файл слишком большой. Максимальный размер: {settings.MAX_FILE_SIZE_MB // (1024 * 1024)} МБ"
            )
        content_type = upload_file.content_type
        if content_type not in allowed_types:
            raise BadRequestException(f"Недопустимый формат файл")
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, system_filename)
        with open(file_path, 'wb') as f:
            f.write(contents)
        new_attach = await AttachmentRepository(self.session).add_file(
            system_filename=system_filename,
            user_filename=upload_file.filename,
            user_id=user_id,
            attach_type=attachment_type
        )
        return new_attach

    async def get_user_icon_file(self, user_id: int):
        user = await UserRepository(self.session).get_by_id(user_id)
        if user is None:
            raise NotFoundException("Пользователь не найден")
        attach_id = user.icon_id
        print(attach_id)
        attachment = await AttachmentRepository(self.session).get(attach_id)
        if attachment is None:
            raise BadRequestException("Такой иконки нет. Дефолтная иконка")
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, attachment.system_filename)
        print(file_path)
        if not os.path.exists(file_path):
            raise NotFoundException("Вложение не найдено на сервере")
        return file_path
    
    async def get_project_icon_file(self, project_id: int):
        project = await ProjectRepository(self.session).get_project(project_id)
        if project is None:
            raise NotFoundException("Проект не найден")
        attach_id = project.icon_id
        attachment = await AttachmentRepository(self.session).get(attach_id)
        if attachment is None:
            raise BadRequestException("Такой иконки нет. Дефолтная иконка")
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, attachment.system_filename)
        if not os.path.exists(file_path):
            raise NotFoundException("Вложение не найдено на сервере")
        return file_path