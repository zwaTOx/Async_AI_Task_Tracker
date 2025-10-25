from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.access_config import Action, ResourceType
from src.user_project_association.dependencies import verify_project_action
from .repository import TagRepository
from src.exceptions import NotFoundException

def verify_tag_action(action: Action):
    async def dependency(
        session: DbSession,
        user: CurrentUser,
        project_id: int,
        tag_id: int = None
    ):
        await verify_project_action(
            session=session,
            user=user,
            project_id=project_id,
            action=action,
            resource_type=ResourceType.TAG
        )
        if not tag_id:
            return 
        tag = await TagRepository(session).get(tag_id)
        if not tag or tag.project_id != project_id:
            raise NotFoundException(detail="Тег не найден в проекте")
    return dependency

async def verify_tag_exists(
    session: DbSession,
    project_id: int,
    tag_id: int
):
    tag = await TagRepository(session).get(tag_id)
    if not tag or tag.project_id != project_id:
        raise NotFoundException(detail="Тег не найден в проекте")