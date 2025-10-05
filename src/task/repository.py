from typing import List
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import PermissionException
from .models import Task
from .schemas import TaskCreate, TaskResponse, TaskUpdate

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, project_id: int) -> List[TaskResponse]:
        statement = select(Task).filter(Task.project_id == project_id)
        result = await self.session.exec(statement)
        return result.scalars().all()

    async def get_task(self, task_id: int):
        statement = select(Task).filter(Task.id==task_id)
        result = await self.session.exec(statement)
        return result.scalars().first()

    async def create_task(self, user_id: int, project_id: int, task_data: TaskCreate) -> Task:
        new_task = Task(creator_id=user_id, project_id=project_id, **task_data.model_dump(exclude_none=True))
        self.session.add(new_task)
        await self.session.commit()
        return new_task
    
    async def update_task(self, task_id: int, task_update: TaskUpdate) -> TaskResponse:
        task = await self.get_task(task_id)
        if task is None:
            raise PermissionException
        update_data = task_update.model_dump(exclude_none=True)
        if task_update.performer_id == 0:
            update_data["performer_id"] = None
        for key, value in update_data.items():
            setattr(task, key, value)
        await self.session.commit()
        return task
    
    async def delete_task(self, task_id: int):
        task = await self.get_task(task_id)
        await self.session.delete(task)
        await self.session.commit()