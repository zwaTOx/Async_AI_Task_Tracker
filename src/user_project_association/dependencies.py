from src.database import DbSession
from src.user.dependencies import CurrentUser
from .access_config import ProjectPermissions, ResourceType, UserRole, Action
from src.user_project_association.service import ProjectAssociationService
from src.task.repository import TaskRepository
from src.exceptions import PermissionException

async def verify_project_action(
    session: DbSession,  
    user: CurrentUser,
    project_id: int,
    action: Action,
    resource_type: ResourceType
):
    member = await ProjectAssociationService(session).get_project_member(user.id, project_id)
    user_role = UserRole(member.role)
    resource_permissions = ProjectPermissions.PERMISSIONS.get(resource_type)
    if not resource_permissions:
        raise PermissionException(f"Неизвестный тип ресурса: {resource_type}")
    permission_rule = resource_permissions.get(action)
    if not permission_rule:
        raise PermissionException(f"Действие {action.value} не разрешено для ресурса {resource_type.value}")
    if permission_rule.is_author:
        return
    if user_role not in permission_rule.roles:
        raise PermissionException(f"Недостаточно прав для выполнения действия {action.value}")
    return user_role

async def verify_project_admin(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int
):
    """Зависимость для проверки прав администратора/владельца проекта."""
    if not await ProjectAssociationService(session).is_project_roles(
        user_id=current_user.id, 
        project_id=project_id
    ):
        raise PermissionException("Недостаточно прав для выполнения данного действия")
    
async def verify_project_member(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int
):
    """Зависимость для проверки членства в проекте."""
    await ProjectAssociationService(session).get_project_member(current_user.id, project_id)

async def verify_create_task_perms(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int):
    if await ProjectAssociationService(session).is_project_roles(
        user_id=current_user.id, 
        project_id=project_id,
        roles=["READER"]
    ):
        raise PermissionException("Недостаточно прав для выполнения данного действия")
    