from sqlalchemy.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException
from .schemes import CategoryCreate, CategoryUpdate, CategoryResponse
from .repository import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_categories(self, user_id: int) -> list[CategoryResponse]:
        categories = await CategoryRepository(self.session).get_categories(user_id) 
        return categories

    async def create_category(self, 
            user_id: int, category_data: CategoryCreate) -> CategoryResponse:
        new_cat = await CategoryRepository(self.session).create_category(user_id, category_data)
        return new_cat
    
    async def update_category(self,
        user_id: int, category_id: int, category_update: CategoryUpdate
    ):
        category = await CategoryRepository(self.session).get_user_category(user_id, category_id)
        if category is None:
            raise NotFoundException("Категория не найдена")
        upd_category = await CategoryRepository(self.session).\
            update_category(user_id, category_id, category_update)
        return upd_category