from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import UserProjectAssociation
from .schemes import InviteProjectData
from .utils import Role

class UserProjectAssociationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_memberships(self, project_id: int):
        statement = select(UserProjectAssociation).filter(UserProjectAssociation.project_id==project_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_membership(self, user_id: int, project_id: int):
        statement = select(UserProjectAssociation).filter(UserProjectAssociation.user_id == user_id, UserProjectAssociation.project_id==project_id)
        result = await self.session.exec(statement)
        return result.first()

    async def register_project_owner(self, user_id: int, project_id: int):
        new_assoc = UserProjectAssociation(
            user_id=user_id,
            project_id=project_id,
            role = "OWNER"
        )
        print(new_assoc)
        self.session.add(new_assoc)
        await self.session.commit()
        print(f"Association created: {new_assoc.id}")
        return new_assoc
    
    async def register_invited_user(self, project_data: InviteProjectData
    ):
        new_assoc = UserProjectAssociation(
            **project_data.model_dump()
        )
        self.session.add(new_assoc)
        await self.session.commit()
        print(f"Association created: {new_assoc.id}")
        return new_assoc

    async def delete_member(self, member_id: int, project_id):
        membership = await self.get_membership(member_id, project_id)
        await self.session.delete(membership)
        await self.session.commit()