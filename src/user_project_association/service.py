from sqlalchemy.ext.asyncio.session import AsyncSession

class ProjectAssociationService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def get_project_members(self, user_id: int, project_id: int):
        pass