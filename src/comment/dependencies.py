from src.user_project_association.dependencies import verify_project_action
from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.exceptions import NotFoundException, BadRequestException, PermissionException
from .repository import CommentRepository
from src.user_project_association.access_config import Action, ResourceType

def verify_comment_creation():
    async def dependency(
        session: DbSession,
        user: CurrentUser,
        project_id: int,
        task_id: int,
        comment_id: int = None  
    ):
        await verify_project_action(
            session=session,
            user=user,
            project_id=project_id,
            action=Action.CREATE,
            resource_type=ResourceType.COMMENT
        )       
        if comment_id:
            parent_comment = await CommentRepository(session).get(comment_id)
            if parent_comment is None or parent_comment.task_id != task_id:
                raise NotFoundException("Родительский комментарий не найден")
            if parent_comment.parent_comment_id is not None:
                raise BadRequestException("Нельзя создавать ответы на ответы")
    
    return dependency

def verify_comment_modification(action: Action):
    async def dependency(
        session: DbSession,
        user: CurrentUser,
        project_id: int,
        task_id: int,
        comment_id: int  
    ):
        await verify_project_action(
            session=session,
            user=user,
            project_id=project_id,
            action=action,
            resource_type=ResourceType.COMMENT
        )
        comment = await CommentRepository(session).get(comment_id)
        if comment is None or comment.task_id != task_id:
            raise NotFoundException("Комментарий не найден")        
        if comment.owner_id != user.id:
            raise PermissionException("Вы можете редактировать только свои комментарии")
    
    return dependency