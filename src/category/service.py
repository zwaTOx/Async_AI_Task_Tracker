from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.exceptions import NotFoundException, BadRequestException
from .schemes import CategoryCreate, CategoryUpdate, CategoryResponse
from .repository import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_categories(self, user_id: int):
        categories = await CategoryRepository(self.session).get_user_categories_with_projects(user_id) 
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

    async def add_project_to_category(self, user_id: int, category_id: int, project_id: int):
        category = await CategoryRepository(self.session).get_category(category_id, user_id)
        if not CategoryRepository(self.session).check_project_in_category(project_id, user_id):
            raise BadRequestException("Проект уже добавлен в категорию")
        if not category:
            raise NotFoundException("Категория не найдена")
        await CategoryRepository(self.session).add_project_to_category(category_id, project_id)
        return category