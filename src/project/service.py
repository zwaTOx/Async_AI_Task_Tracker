from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException, PermissionException
from src.user_project_association.repository import UserProjectAssociationRepository
from .schemes import ProjectCreate, ProjectUpdate
from .repository import ProjectRepository


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_project(self, user_id: int, project_data: ProjectCreate):
        new_project = await ProjectRepository(self.session).create_project(user_id, project_data)
        await UserProjectAssociationRepository(self.session).register_project_owner(user_id, new_project.id)
        return new_project

    async def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdate):
        updated_project = await ProjectRepository(self.session).update_project(
            user_id, project_id, project_data)
        return updated_project
    
    async def delete_project(self, user_id: int, project_id: int):
        project = await ProjectRepository(self.session).get_project(project_id)
        if project.owner_id != user_id:
            raise PermissionError
        await ProjectRepository(self.session).delete_project(project_id)