from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.exceptions import PermissionException, NotFoundException, BadRequestException, IternalServerException
from src.user.repository import UserRepository
from src.code.utils import create_invite_project_token, decode_invite_project_token
from src.email.invite import send_project_invite
from src.category.repository import CategoryRepository
from .schemes import InviteModel, UpdateMemberData, MembershipResponse
from .repository import UserProjectAssociationRepository
from src.config import settings

class ProjectAssociationService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def is_project_roles(self, 
            project_id: int, 
            user_id: int, 
            roles: list[str] = ['ADMINISTRATOR', "OWNER"]) -> bool:
        membership = await UserProjectAssociationRepository(self.session).get_membership(user_id, project_id)
        if membership is None:
            raise PermissionException("Недостаточно прав для выполения операции")
        return membership.role in roles

    async def get_project_members(self, 
        user_id: int, 
        project_id: int
    ) -> MembershipResponse:
        memberships = await UserProjectAssociationRepository(self.session).get_project_memberships(project_id)
        return memberships
    
    async def get_project_member(self,
        user_id: int,
        project_id: int
    ):
        membership = await UserProjectAssociationRepository(self.session).get_membership(user_id, project_id)
        if membership is None:
            raise PermissionException
        return membership

    async def invite_member_by_email(self, 
        user, 
        project_id: int, 
        inv_email: str,
        inv_role: str
        ):
        membership = await UserProjectAssociationRepository(self.session).get_membership(user.id, project_id)
        if membership is None:
            raise PermissionException
        
        founded_user = await UserRepository(self.session).get_user_by_email(inv_email)
        if founded_user is None:
            raise NotFoundException("Данный пользователь не зарегистрирован в приложении")

        inviter_membership = await UserProjectAssociationRepository(self.session).\
            get_membership(founded_user.id, project_id)
        if inviter_membership is not None:
            raise BadRequestException("Пользователь уже является частью проекта")
        invite_token = create_invite_project_token(project_id, founded_user.id, inv_role)
        url = f"{settings.BASE_URL}/users/invite?access_token={invite_token}"
        result = send_project_invite(founded_user.email, "Noname", "Noname", url)
        if not result:
            raise IternalServerException
        
    async def confirm_invite(self, 
        invite_token: str
    ):
        project_data = decode_invite_project_token(invite_token)
        membership = await UserProjectAssociationRepository(self.session).\
            get_membership(project_data.user_id, project_data.project_id)
        if membership is not None:
            raise BadRequestException("Пользователь уже является частью проекта")
        new_assos = await UserProjectAssociationRepository(self.session).register_invited_user(project_data)
        return new_assos
    
    async def update_project_member(self,
        user_id: int, project_id: int, member_id: int, update_data: UpdateMemberData) -> MembershipResponse:
        membership = await UserProjectAssociationRepository(self.session).\
            get_membership(member_id, project_id)
        if membership is None:
            raise BadRequestException("Пользователь не является частью проекта")
        if membership.user_id == user_id:
            raise BadRequestException("Вы не можете обновить свои роли в проекте #ВРЕМЕННО")
        if membership.role == "OWNER":
            raise PermissionException("Недостаточно прав для совершения этого действия")
        upd_membership = await UserProjectAssociationRepository(self.session).\
            update_member(member_id, project_id, update_data)
        return upd_membership

    async def delete_project_member(self,
            user_id: int, project_id: int, del_user_id: int):
        del_user = await UserRepository(self.session).get_by_id(del_user_id)
        if del_user is None:
            raise NotFoundException
        del_membership = await UserProjectAssociationRepository(self.session).\
            get_membership(del_user.id, project_id)
        if del_membership is None:
            raise BadRequestException("Пользователь не является частью проекта")
        if del_membership.user_id == user_id:
            raise BadRequestException("Вы не можете кикнуть себя из проекта")
        if del_membership.role == "OWNER":
            raise PermissionException("Недостаточно прав для совершения этого действия")
        await UserProjectAssociationRepository(self.session).delete_member(del_user_id, project_id)
        
    async def leave_project(self,
        user_id: int, project_id: int
    ):
        membership = await self.get_project_member(user_id, project_id)
        if membership.role == "OWNER":
            raise BadRequestException("Создатель проекта не может выйти из проекта")
        await UserProjectAssociationRepository(self.session).delete_member(user_id, project_id)
        
        