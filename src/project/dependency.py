from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_action as verify_base_action
from src.user_project_association.access_config import Action, ResourceType


def verify_project_action(action: Action):
    async def dependency(
        session: DbSession,
        user: CurrentUser,
        project_id: int = None,
    ):
        await verify_base_action(
            session=session,
            user=user,
            project_id=project_id,
            action=action,
            resource_type=ResourceType.PROJECT
        )
    return dependency