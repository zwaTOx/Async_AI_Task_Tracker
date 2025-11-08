from src.database import DbSession
from src.exceptions import PermissionException, NotFoundException
from src.user.dependencies import CurrentUser
from src.user_project_association.access_config import Action, ResourceType, UserRole
from src.user_project_association.dependencies import verify_project_action
from src.user_project_association.service import ProjectAssociationService
from src.task.repository import TaskRepository

def verify_task_action(action: Action):
    async def dependency(
        session: DbSession,
        user: CurrentUser,
        project_id: int,
        task_id: int = None
    ):
        user_role = await verify_project_action(
            session=session,
            user=user,
            project_id=project_id,
            action=action,
            resource_type=ResourceType.TASK
        )
        if action in [Action.CREATE, Action.VIEW]:
            return
        task = await TaskRepository(session).get_task(task_id)
        if not task or task.project_id != project_id: 
            raise NotFoundException('Задача не найдена в прокте')
        print([user_role, UserRole.OWNER])
        if user_role in [UserRole.ADMINISTRATOR.value, UserRole.OWNER.value]:
            return
        if action == Action.DELETE:
            if task.creator_id != user.id:
                raise PermissionException(f"Недостаточно прав для выполнения действия")
        if action == Action.EDIT:
            print([task.performer_id, task.creator_id])
            if user.id not in [task.performer_id, task.creator_id]:
                raise PermissionException(f"Недостаточно прав для выполнения действия!")
    return dependency

async def verify_task_exists(
    session: DbSession,
    task_id: int,
    project_id: int   
):
    is_task_exist = await TaskRepository(session).get(task_id)
    if not is_task_exist:
        raise NotFoundException("Задача не найдена")

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