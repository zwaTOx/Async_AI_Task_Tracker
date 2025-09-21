from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemes import ProjectCreate
from .models import Project

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_project(self, user_id: int, project_data: ProjectCreate) -> Project:
        new_project = Project(owner_id=user_id, **project_data.model_dump())
        self.session.add(new_project)
        await self.session.commit()
        return new_project
    
    async def get_projects(self, user_id: int) -> list[Project]:
        statement = select(Project).filter(Project.owner_id == user_id)
        result = await self.session.exec(statement)
        return result.all()