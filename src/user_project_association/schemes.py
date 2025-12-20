from datetime import datetime
from typing import Optional
from src.schemas import CustomBase
from pydantic import Field
from fastapi import Query

from src.user.schemes import UserResponse
from .utils import Roles, Inv_Roles, Update_Roles
from src.config import settings

class InviteModel(CustomBase):
    email: str 
    role: Inv_Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)

class InviteProjectData(CustomBase):
    user_id: int
    role: Inv_Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
    project_id: int

class MembershipResponse(CustomBase):
    id: int
    category_id: Optional[int] = Field(default=None)
    project_id: int
    role: Roles
    joined_at: datetime

class MembershipWithUserResponse(MembershipResponse):
    user: UserResponse

class MembershipPagination(CustomBase):
    items: list[MembershipWithUserResponse]

class UpdateMemberData(CustomBase):
    role: Update_Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
