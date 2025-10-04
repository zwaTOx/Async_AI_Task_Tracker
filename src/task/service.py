from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import BadRequestException
from .schemas import TaskCreate, TaskResponse
from src.user_project_association.repository import UserProjectAssociationRepository
from .repository import TaskRepository

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, project_id: int) -> List[TaskResponse]:
        tasks = await TaskRepository(self.session).get_tasks(project_id)
        return tasks

    async def create_task(self,
            user_id: int, project_id: int, task_create: TaskCreate): 
        if task_create.performer_id is not None:
            performer = await UserProjectAssociationRepository(self.session).get_membership(task_create.performer_id, project_id)
            if performer is None:
                raise BadRequestException("Исполнитель не является участником проекта")
        new_task = await TaskRepository(self.session).create_task(user_id, project_id, task_create)
        return new_task