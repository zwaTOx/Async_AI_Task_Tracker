from typing import List
from sqlalchemy import update
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import delete, select
from sqlalchemy.orm import selectinload

from src.project.models import Project
from src.user_project_association.models import UserProjectAssociation
from src.category.models import project_category
from .models import Category
from .schemes import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_categories_with_projects(self, user_id: int):
        statement = (
            select(Category)
            .options(selectinload(Category.projects))
            .where(Category.user_id == user_id)
        )
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_user_projects_without_categories(self, user_id: int) -> list[Project]:
        projects_with_categories_subquery = (
        select(project_category.c.project_id)
        .distinct()
        .subquery()
        )
        
        statement = (
            select(Project)
            .join(UserProjectAssociation, Project.id == UserProjectAssociation.project_id)
            .where(
                (UserProjectAssociation.user_id == user_id) &
                (~Project.id.in_(select(projects_with_categories_subquery.c.project_id)))
            )
        )
        result = await self.session.exec(statement)
        return result.all()

    async def check_project_in_category(self, project_id: int, user_id: int):
        statement = (
            select(Category)
            .join(project_category, Category.id == project_category.c.category_id)
            .where(
                (project_category.c.project_id == project_id) &
                (Category.user_id == user_id)
            )
        )
        result = await self.session.exec(statement)
        return result.first() is not None
    
    async def add_project_to_category(self, category_id: int, project_id: int):
        insert_stmt = project_category.insert().values(
            category_id=category_id,
            project_id=project_id
        )
        await self.session.exec(insert_stmt)
        await self.session.commit()

    async def get_categories(self, user_id: int):
        statement = select(Category).filter(Category.user_id==user_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_category(self, category_id: int, user_id: int):
        statement = select(Category).filter(Category.id==category_id, Category.user_id==user_id)
        result = await self.session.exec(statement)
        return result.first()

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
    
    async def delete_category(self, category_id: int):
        statement = delete(Category).where(Category.id == category_id)
        await self.session.exec(statement)
        await self.session.commit()