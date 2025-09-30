from sqlalchemy.ext.asyncio.session import AsyncSession

from .schemes import CategoryCreate
from .repository import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_categories(self, user_id: int):
        categories = await CategoryRepository(self.session).get_categories(user_id) 
        return categories

    async def create_category(self, 
            user_id: int, category_data: CategoryCreate):
        new_cat = await CategoryRepository(self.session).create_category(user_id, category_data)
        return new_cat