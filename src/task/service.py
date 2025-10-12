from datetime import datetime
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exceptions import BadRequestException, PermissionException
from .schemas import TaskCreate, TaskResponse, TaskResponseWithSubtasks, TaskUpdate
from src.user_project_association.repository import UserProjectAssociationRepository
from src.project.repository import ProjectRepository
from .repository import TaskRepository

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, project_id: int) -> List[TaskResponse]:
        tasks = await TaskRepository(self.session).get_tasks(project_id)
        return tasks

    async def get_tasks_by_date_range(self, 
        user_id: int, 
        project_ids: Optional[List[int]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[TaskResponse]:
        user_projects = await ProjectRepository(self.session).get_projects(user_id)
        user_project_ids = [project.id for project in user_projects]
        
        if project_ids:
            invalid_projects = set(project_ids) - set(user_project_ids)
            if invalid_projects:
                raise PermissionException(f"Нет доступа к проектам: {invalid_projects}")
            final_project_ids = project_ids
        else:
            #Используем все проекты
            final_project_ids = user_project_ids
        tasks = await TaskRepository(self.session).get_tasks_by_date_range(
        user_id=user_id,
        project_ids=final_project_ids,
        start_date=start_date,
        end_date=end_date
    )
        return tasks

    async def get_task_by_id(self, project_id: int, task_id: int) -> TaskResponseWithSubtasks:
        task = await TaskRepository(self.session).get_task_with_subtasks(task_id)
        if task is None or task.project_id != project_id:
            raise BadRequestException("Задача не найдена")
        return task

    async def create_task(self,
            user_id: int, project_id: int, task_create: TaskCreate): 
        if task_create.performer_id is not None:
            performer = await UserProjectAssociationRepository(self.session).get_membership(task_create.performer_id, project_id)
            if performer is None:
                raise BadRequestException("Исполнитель не является участником проекта")
        if task_create.start and task_create.end:
            if task_create.start > task_create.end:
                raise BadRequestException("Дата начала не может быть позже даты окончания")
        new_task = await TaskRepository(self.session).create_task(user_id, project_id, task_create)
        return new_task
    
    async def update_task(self,
            user_id: int, project_id: int, task_id: int, task_update: TaskUpdate):
        if task_update.performer_id is not None and task_update.performer_id!=0:
            performer = await UserProjectAssociationRepository(self.session).get_membership(task_update.performer_id, project_id)
            if performer is None:
                raise BadRequestException("Исполнитель не является участником проекта")
        upd_task = await TaskRepository(self.session).update_task(task_id, task_update)
        return upd_task
        
    async def delete_task(self, user_id: int, project_id: int, task_id: int):
        await TaskRepository(self.session).delete_task(task_id)