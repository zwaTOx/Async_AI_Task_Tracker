from enum import Enum
from typing import Dict, List, Set, Callable, Any
from dataclasses import dataclass

class UserRole(Enum):
    READER = "READER"
    MEMBER = "USER"
    ADMINISTRATOR = "ADMINISTRATOR"
    OWNER = "OWNER"

class ResourceType(Enum):
    PROJECT = "project"
    TASK = "task"
    COMMENT = "comment"
    TAG = 'tag'
    IDEA = 'idea'

class Action(Enum):
    VIEW = "view"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    MANAGE = "manage"  # Управление (назначение прав и т.д.)

class PermissionRule:
    """Правило разрешения"""
    def __init__(
        self, 
        roles: Set[UserRole] = None,
        is_project_owner: bool = False,
        is_author: bool = False,
        custom_check: callable = None
    ):
        self.roles = roles or set(UserRole)  # По умолчанию все роли
        self.is_project_owner = is_project_owner
        self.is_author = is_author
        self.custom_check = custom_check

class ProjectPermissions:
    """Конфигурация прав доступа для проекта"""
    PERMISSIONS: Dict[ResourceType, Dict[Action, PermissionRule]] = {
        ResourceType.PROJECT: {
            Action.VIEW: PermissionRule(),
            Action.EDIT: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
            Action.DELETE: PermissionRule(roles={
                UserRole.OWNER
            }),
            Action.MANAGE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
        },
        ResourceType.TASK: {
            Action.VIEW: PermissionRule(),
            Action.CREATE: PermissionRule(roles={
                UserRole.MEMBER, UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
            Action.EDIT: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }, is_author=True), 
            Action.DELETE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }, is_author=True),
        },
        ResourceType.TAG: {
            Action.VIEW: PermissionRule(),
            Action.CREATE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
            Action.EDIT: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
            Action.DELETE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
        },
        ResourceType.COMMENT: {
            Action.VIEW: PermissionRule(),
            Action.CREATE: PermissionRule(),
            Action.EDIT: PermissionRule(is_author=True), 
            Action.DELETE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }, is_author=True),  
        },
        ResourceType.IDEA: {
            Action.VIEW: PermissionRule(),
            Action.CREATE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }),
            Action.EDIT: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }, is_author=True), 
            Action.DELETE: PermissionRule(roles={
                UserRole.ADMINISTRATOR, UserRole.OWNER
            }, is_author=True),
        },
    }