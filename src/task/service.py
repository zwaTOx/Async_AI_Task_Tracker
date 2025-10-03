from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TaskCreate, TaskResponse
from src.user_project_association.service import ProjectAssociationService
from .repository import TaskRepository

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, project_id: int) -> List[TaskResponse]:
        tasks = await TaskRepository(self.session).get_tasks(project_id)
        return tasks

    async def create_task(self,
            user_id: int, project_id: int, task_create: TaskCreate): 
        await ProjectAssociationService(self.session).get_project_member(user_id, project_id)
        new_task = await TaskRepository(self.session).create_task(user_id, project_id, task_create)
        return new_task