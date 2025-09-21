from sqlmodel.ext.asyncio.session import AsyncSession

from .schemes import ProjectCreate

class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create_project(user_id: int, project_data: ProjectCreate):
