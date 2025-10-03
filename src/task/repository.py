from typing import List
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Task
from .schemas import TaskCreate, TaskResponse

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, project_id: int) -> List[Task]:
        statement = select(Task).filter(Task.project_id == project_id)
        result = await self.session.exec(statement)
        return result.scalars().all()

    async def create_task(self, user_id: int, project_id: int, task_data: TaskCreate) -> Task:
        new_task = Task(creator_id=user_id, project_id=project_id, **task_data.model_dump(exclude_none=True))
        self.session.add(new_task)
        await self.session.commit()
        return new_task