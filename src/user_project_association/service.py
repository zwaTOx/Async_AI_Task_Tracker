from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.exceptions import PermissionException, NotFoundException, BadRequestException, IternalServerException
from src.user.repository import UserRepository
from src.code.utils import create_invite_project_token
from src.email.invite import send_project_invite
from .schemes import InviteModel
from .repository import UserProjectAssociationRepository

class ProjectAssociationService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_project_members(self, 
        user_id: int, 
        project_id: int
    ):
        membership = await UserProjectAssociationRepository(self.session).get_membership(user_id, project_id)
        if membership is None:
            raise PermissionException
        memberships = await UserProjectAssociationRepository(self.session).get_project_memberships(project_id)
        return memberships
    
    async def invite_member_by_email(self, 
        request: Request, 
        user, 
        project_id: int, 
        invitation_request: InviteModel):
        membership = await UserProjectAssociationRepository(self.session).get_membership(user.id, project_id)
        if membership is None:
            raise PermissionException
        
        founded_user = await UserRepository(self.session).get_user_by_email(invitation_request.email)
        if founded_user is None:
            raise NotFoundException
        
        inviter_membership = await UserProjectAssociationRepository(self.session).\
            get_membership(founded_user.id, project_id)
        if inviter_membership is not None:
            raise BadRequestException("The user is already a member of the project")
        invite_token = create_invite_project_token(founded_user.id, project_id)
        url = f"{request.base_url}/users/invite?access_token={invite_token}"
        result = send_project_invite(founded_user.email, "Noname", "Noname", url)
        if not result:
            raise IternalServerException
        
        