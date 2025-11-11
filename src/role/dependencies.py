from typing import Set

from src.database import DbSession
from src.exceptions import PermissionException
from src.role.config import ACCESS_CONFIG_JSON
from src.user.dependencies import CurrentUser
from src.user_project_association.access_config import Action, ResourceType, UserRole
from src.user_project_association.service import ProjectAssociationService

class ProjectRoleChecker:
    def __init__(self, resource: ResourceType, action: Action):
        self.resource = resource.value
        self.action = action.value
        self.allowed_roles = self._get_allowed_roles()

    def _get_allowed_roles(self) -> Set[UserRole]:
        try:
            return ACCESS_CONFIG_JSON[self.resource][self.action]
        except KeyError:
            raise ValueError(
                f"Не найдена конфигурация прав для ресурса '{self.resource.value}' "
                f"и действия '{self.action.value}'"
            )

    async def __call__(self, 
        project_id: int,
        current_user: CurrentUser,
        session: DbSession):
        member = await ProjectAssociationService(session).get_project_member(current_user.id, project_id)
        if not member:
            raise PermissionException
        if member.role not in self.allowed_roles:
            raise PermissionException(
                detail="Недостаточно прав для выполнения этого действия"
            )
        
        return current_user

#PROJECT
def can_view_project():
    return ProjectRoleChecker(ResourceType.PROJECT, Action.VIEW)

def can_edit_project():
    return ProjectRoleChecker(ResourceType.PROJECT, Action.EDIT)

def can_delete_project():
    return ProjectRoleChecker(ResourceType.PROJECT, Action.DELETE)

def can_manage_project():
    return ProjectRoleChecker(ResourceType.PROJECT, Action.MANAGE)

#TASK
def can_create_task():
    return ProjectRoleChecker(ResourceType.TASK, Action.CREATE)

def can_view_task():
    return ProjectRoleChecker(ResourceType.TASK, Action.VIEW)

def can_edit_task():
    return ProjectRoleChecker(ResourceType.TASK, Action.EDIT)

def can_delete_task():
    return ProjectRoleChecker(ResourceType.TASK, Action.DELETE)

#COMMENT
def can_create_comment():
    return ProjectRoleChecker(ResourceType.COMMENT, Action.CREATE)

def can_view_comment():
    return ProjectRoleChecker(ResourceType.COMMENT, Action.VIEW)

def can_edit_comment():
    return ProjectRoleChecker(ResourceType.COMMENT, Action.EDIT)

def can_delete_comment():
    return ProjectRoleChecker(ResourceType.COMMENT, Action.DELETE)

#TAG
def can_create_tag():
    return ProjectRoleChecker(ResourceType.TAG, Action.CREATE)

def can_view_tag():
    return ProjectRoleChecker(ResourceType.TAG, Action.VIEW)

def can_edit_tag():
    return ProjectRoleChecker(ResourceType.TAG, Action.EDIT)

def can_delete_tag():
    return ProjectRoleChecker(ResourceType.TAG, Action.DELETE)

#IDEA
def can_create_idea():
    return ProjectRoleChecker(ResourceType.IDEA, Action.CREATE)

def can_view_idea():
    return ProjectRoleChecker(ResourceType.IDEA, Action.VIEW)

def can_edit_idea():
    return ProjectRoleChecker(ResourceType.IDEA, Action.EDIT)

def can_delete_idea():
    return ProjectRoleChecker(ResourceType.IDEA, Action.DELETE)