from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession

from src.repository import SQLAlchemyRepository
from src.exceptions import PermissionException
from src.tag.model import Tag
from .models import Task
from .schemas import TaskCreate, TaskResponse, TaskUpdate, TaskResponseWithSubtasks

class TaskRepository(SQLAlchemyRepository):
    model = Task

    async def get_tasks(self, project_id: int) -> List[TaskResponse]:
        statement = select(Task).filter(Task.project_id == project_id)
        result = await self.session.exec(statement)
        return result.scalars().all()

    async def get_tasks_by_date_range(self, 
        user_id: int,
        project_ids: List[int],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        statement = select(Task).where(Task.project_id.in_(project_ids))

        if start_date and end_date:
            start_date_date = start_date.date() if isinstance(start_date, datetime) else start_date
            end_date_date = end_date.date() if isinstance(end_date, datetime) else end_date
        statement = statement.where(
            or_(
                and_(
                    Task.end.isnot(None),
                    func.date(Task.end) >= start_date_date,
                    func.date(Task.end) <= end_date_date
                ),
                and_(
                    Task.start.isnot(None),
                    func.date(Task.start) >= start_date_date,
                    func.date(Task.start) <= end_date_date
                ),
                and_(
                    Task.start.isnot(None),
                    Task.end.isnot(None),
                    func.date(Task.start) <= end_date_date,
                    func.date(Task.end) >= start_date_date
                )
            )
        )
        
        result = await self.session.exec(statement)
        return result.scalars().all()
    
    async def get_task(self, task_id: int):
        statement = select(Task).filter(Task.id==task_id).options(selectinload(Task.tags))
        result = await self.session.exec(statement)
        return result.scalar_one_or_none()

    async def get_task_with_subtasks(self, task_id: int) -> TaskResponseWithSubtasks:
        statement = select(Task).where(Task.id == task_id)\
            .options(
            selectinload(Task.subtasks),
            selectinload(Task.tags),
            joinedload(Task.creator),        
            joinedload(Task.performer)       
        )
        result = await self.session.exec(statement)
        return result.scalars().first()
    
    async def _update_task_tags(self, task, tags: list[int]):
        stmt = select(Tag).where(Tag.id.in_(tags))
        result = await self.session.exec(stmt)
        new_tags = result.scalars().all()
        task.tags = new_tags

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> TaskResponse:
        task = await self.get_task(task_id)
        if task is None:
            raise PermissionException
        update_data = task_update.model_dump(exclude_none=True, exclude='tags')
        if task_update.performer_id == 0:
            update_data["performer_id"] = None
        for key, value in update_data.items():
            setattr(task, key, value)
        if task_update.tags is not None:
            await self._update_task_tags(task, task_update.tags)
        await self.session.commit()
        await self.session.refresh(task)
        return task