from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .models import Category
from .schemes import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories(self, user_id: int):
        statement = select(Category).filter(Category.user_id==user_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_user_category(self, user_id: int, category_id: int):
        statement = select(Category).filter(Category.id==category_id, Category.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_category(self, user_id: int, category_data: CategoryCreate):
        new_categ = Category(
            **category_data.model_dump(),
            user_id=user_id
        )
        self.session.add(new_categ)
        await self.session.commit()
        return new_categ
    
    async def update_category(self, 
        user_id: int, category_id: int,  category_update: CategoryUpdate):
        category = await self.get_user_category(user_id, category_id)
        update_data = category_update.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(category, key, value)
        await self.session.commit()
        return category
    