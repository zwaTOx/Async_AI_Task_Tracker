from sqlmodel.ext.asyncio.session import AsyncSession

from .schemes import ProjectUpdate
from .repository import ProjectRepository


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdate):
        updated_project = await ProjectRepository(self.session).update_project(
            user_id, project_id, project_data)
        return updated_project