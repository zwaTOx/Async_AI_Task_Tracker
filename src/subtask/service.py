from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException, PermissionException
from src.task.repository import TaskRepository
from .repository import SubtaskRepository
from .schemas import SubtaskCreate, SubtaskResponse, SubtaskUpdate

class SubtaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_subtasks(self, task_id: int):
        task = await TaskRepository(self.session).get_task(task_id)
        if not task:
            raise NotFoundException("Задача не найдена")
        subtasks = await SubtaskRepository(self.session).get_all(task_id=task_id)
        return subtasks
    
    async def create_subtask(self, task_id: int, subtask_data: SubtaskCreate):
        new_subtask = await SubtaskRepository(self.session).create(subtask_data, task_id=task_id)
        return new_subtask
    
    async def update_subtask(self, subtask_id: int, subtask_data: SubtaskUpdate):
        subtask = await SubtaskRepository(self.session).get(subtask_id)
        if not subtask:
            raise NotFoundException("Подзадача не найдена")
        upd_subtask = await SubtaskRepository(self.session).update(subtask_id, subtask_data)
        return upd_subtask
    
    async def delete_subtask(self, subtask_id: int):
        subtask = await SubtaskRepository(self.session).get(subtask_id)
        if not subtask:
            raise NotFoundException("Подзадача не найдена")
        await SubtaskRepository(self.session).delete(subtask_id)
        return None