from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException
from .repository import TagRepository
from .schemes import TagCreate, TagResponse, TagUpdate

class TagService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_project_tags(self, project_id: int) -> List[TagResponse]:
        tags = await TagRepository(self.session).get_all(project_id=project_id)
        return tags
    
    async def create_tag(self, project_id: int, tag_data: TagCreate) -> TagResponse:
        new_tag = await TagRepository(self.session).create(tag_data, project_id=project_id)
        return new_tag
    
    async def update_tag(self, tag_id: int, tag_data: TagUpdate) -> TagResponse:
        upd_tag = await TagRepository(self.session).update(tag_id, tag_data)
        return upd_tag
    
    async def delete_tag(self, tag_id: int):
        await TagRepository(self.session).delete(tag_id)