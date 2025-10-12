from typing import Any, Dict
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.exec(query)
        return result.scalar_one_or_none()

    async def get_all(self, **filters: Dict[str, Any]):
        query = select(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: BaseModel, **extra_fields: Dict[str, Any]):
        instance_data = data.model_dump(exclude_none=True)
        instance_data.update(extra_fields)
        
        instance = self.model(**instance_data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


    async def update(self, id: int, data: BaseModel):
        instance = await self.get(id)
        if instance:
            update_data = data.model_dump(exclude_none=True)
            for key, value in update_data.items():
                setattr(instance, key, value)
            await self.session.commit()
            await self.session.refresh(instance)
        return instance

    async def delete(self, id: int):
        instance = await self.get(id)
        if not instance:
            return False
        await self.session.delete(instance)
        await self.session.commit()
        return True