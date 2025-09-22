from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException, PermissionException
from .schemes import ProjectUpdate
from .repository import ProjectRepository


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdate):
        updated_project = await ProjectRepository(self.session).update_project(
            user_id, project_id, project_data)
        return updated_project
    
    async def delete_project(self, user_id: int, project_id: int):
        project = await ProjectRepository(self.session).get_project(user_id, project_id)
        if not project:
            raise NotFoundException("Проект не найден")
        await ProjectRepository(self.session).delete_project(project)