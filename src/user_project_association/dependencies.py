from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.service import ProjectAssociationService
from src.exceptions import PermissionException

async def verify_project_admin(
    session: DbSession,
    current_user: CurrentUser,
    project_id: int
):
    """Зависимость для проверки прав администратора/владельца проекта."""
    if not await ProjectAssociationService(session).is_project_admin_or_owner(
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
