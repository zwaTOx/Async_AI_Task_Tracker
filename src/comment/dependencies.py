from src.user_project_association.dependencies import verify_project_action
from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.exceptions import NotFoundException
from .repository import CommentRepository
from src.user_project_association.access_config import Action, ResourceType

def verify_comment_action(action: Action):
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
            action=action,
            resource_type=ResourceType.COMMENT
        )
        if action not in [Action.DELETE, Action.EDIT]:
            return
        comment = await CommentRepository(session).get(comment_id)
        if comment is None or comment.task_id!=task_id:
            raise NotFoundException("Комментарий не найден в проекте или в задаче")
    return dependency