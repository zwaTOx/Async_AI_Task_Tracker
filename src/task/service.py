from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import BadRequestException, NotFoundException
from .schemas import TaskCreate, TaskResponse, TaskUpdate
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
    
    async def update_task(self,
            user_id: int, project_id: int, task_id: int, task_update: TaskUpdate):
        membership = await UserProjectAssociationRepository(self.session).get_membership(user_id, project_id)
        task = await TaskRepository(self.session).get_task(task_id)
        if task is None or task.project_id != project_id:
            raise NotFoundException("Задача не найдена в проекте")
        if membership.role == "USER" and task.creator_id != user_id:
            raise PermissionError("Недостаточно прав для выполнения данной операции")
        elif task_update.performer_id is not None and task_update.performer_id!=0:
            performer = await UserProjectAssociationRepository(self.session).get_membership(task_update.performer_id, project_id)
            if performer is None:
                raise BadRequestException("Исполнитель не является участником проекта")
        upd_task = await TaskRepository(self.session).update_task(task_id, task_update)
        return upd_task
        