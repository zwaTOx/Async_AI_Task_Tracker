from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import PermissionException
from src.user_project_association.models import UserProjectAssociation

from .schemes import ProjectCreate, ProjectUpdate
from .models import Project

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project(self, user_id: int, project_id: int) -> Project:
        statement = select(Project).filter(Project.owner_id == user_id, Project.id == project_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_project(self, user_id: int, project_data: ProjectCreate) -> Project:
        new_project = Project(owner_id=user_id, **project_data.model_dump())
        self.session.add(new_project)
        await self.session.commit()
        return new_project
    
    async def get_projects(self, user_id: int) -> list[Project]:
        statement = select(Project)\
        .join(UserProjectAssociation, Project.id == UserProjectAssociation.project_id)\
        .where(UserProjectAssociation.user_id == user_id)
        result = await self.session.exec(statement)
        return result.all()
    
    async def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdate):
        project = await self.get_project(user_id, project_id)
        if project is None:
            raise PermissionException
        update_data = project_data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(project, key, value)
        await self.session.commit()
        return project
    
    async def delete_project(self, project):
        await self.session.delete(project)
        await self.session.commit()