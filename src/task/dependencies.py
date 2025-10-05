from src.database import DbSession
from src.exceptions import PermissionException, NotFoundException
from src.user.dependencies import CurrentUser
from src.user_project_association.service import ProjectAssociationService
from src.task.repository import TaskRepository


async def verify_update_task_perms(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int,
    task_id: int
):
    if await ProjectAssociationService(session).is_project_roles(
        user_id=current_user.id, 
        project_id=project_id,
        roles=["READER"]):
        raise PermissionException("Недостаточно прав для выполнения данного действия")
    membership = await ProjectAssociationService(session).get_project_member(current_user.id, project_id)
    task = await TaskRepository(session).get_task(task_id)
    if task is None or task.project_id!=project_id:
        raise NotFoundException("Задача не найдена в текущем проекте")
    if membership.role == "USER" and current_user.id!=task.creator_id:
        raise PermissionException("Недостаточно прав для выполнения данного действия")