from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemes import UserCreate, UserUpdateData
from .utils import hash_password

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str):
        statement = select(User).filter(User.id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_user_by_email(self, user_email: str):
        statement = select(User).filter(User.email == user_email)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_user_by_username(self, username: str):
        statement = select(User).filter(User.username == username)
        result = await self.session.exec(statement)
        return result.first()

    async def create_user(self, user_data: UserCreate):
        hashed_password = hash_password(user_data.password) 
        data_dict = user_data.model_dump(exclude={'password', 'verify_password'})
        new_user = User(hashed_password=hashed_password, nickname=user_data.username[1:], **data_dict)
        self.session.add(new_user)
        await self.session.commit()
        return new_user
    
    async def update_user_info(self, user_id: int, user_data: UserUpdateData):
        user = await self.get_by_id(user_id)
        update_data = user_data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def update_password(self, user_id, new_password: str):
        new_hashed_password = hash_password(new_password) 
        user = await self.get_by_id(user_id)
        user.hashed_password = new_hashed_password
        self.session.add(user)
        await self.session.commit()