from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, mapped_column, declared_attr, DeclarativeBase
from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False
)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_session():
    async with async_session() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_session)]

int_pk = Annotated[int, mapped_column(primary_key=True)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    