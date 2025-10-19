from src.database import DbSession
from src.exceptions import PermissionException, NotFoundException
from src.user.dependencies import CurrentUser
from src.user_project_association.service import ProjectAssociationService
from src.task.repository import TaskRepository

async def verify_task_perms_base(
    session: DbSession,
    user_id: int,
    project_id: int,
    task_id: int
):
    membership = await ProjectAssociationService(session).get_project_member(user_id, project_id)
    if membership.role=="READER":
        PermissionException("Недостаточно прав для выполнения данного действия")
    task = await TaskRepository(session).get_task(task_id)
    if task is None or task.project_id!=project_id:
        raise NotFoundException("Задача не найдена в текущем проекте")
    return membership, task

async def verify_update_task_perms(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int,
    task_id: int
):
    membership, task = await verify_task_perms_base(session, current_user.id, project_id, task_id)
    if membership.role == "USER" and current_user.id!=task.creator_id and current_user.id!=task.performer_id:
        raise PermissionException("Недостаточно прав для выполнения данного действия")
    
async def verify_delete_task_perms(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int,
    task_id: int
):
    membership, task = await verify_task_perms_base(session, current_user.id, project_id, task_id)
    if membership.role == "USER" and current_user.id!=task.creator_id:
        raise PermissionException("Недостаточно прав для выполнения данного действия")