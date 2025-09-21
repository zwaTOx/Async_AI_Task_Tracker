from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemes import UserCreate
from .utils import hash_password

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str):
        stmt = select(User).filter(User.id == user_id)
        result = await self.session.exec(stmt)
        return result.first()

    async def get_user_by_email(self, user_email: str):
        statement = select(User).filter(User.email == user_email)
        result = await self.session.exec(statement)
        return result.first()
    
    async def create_user(self, user_data: UserCreate):
        hashed_password = hash_password(user_data.password) 
        data_dict = user_data.model_dump(exclude={'password', 'verify_password'})
        new_user = User(hashed_password=hashed_password, **data_dict)
        self.session.add(new_user)
        await self.session.commit()
        return new_user
    