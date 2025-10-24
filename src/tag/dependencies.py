from src.database import DbSession

from .repository import TagRepository
from src.exceptions import NotFoundException

async def verify_tag_exists(
    session: DbSession,
    project_id: int,
    tag_id: int
):
    tag = await TagRepository(session).get(tag_id)
    if not tag or tag.project_id != project_id:
        raise NotFoundException(detail="Тег не найден в проекте")