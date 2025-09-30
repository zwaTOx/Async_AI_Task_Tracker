from datetime import datetime
from typing import Optional
from src.models import CustomBase
from pydantic import Field
from fastapi import Query
from .utils import Roles, Inv_Roles, Update_Roles
from src.config import settings

class InviteModel(CustomBase):
    email: str = Query(...)
    role: Inv_Roles = Query(default=settings.DEFAULT_PROJECT_ROLE)

class InviteProjectData(CustomBase):
    user_id: int
    role: Inv_Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
    project_id: int

class MembershipResponse(CustomBase):
    id: int
    user_id: int
    category_id: Optional[int] = Field(default=None)
    project_id: int
    role: Roles
    joined_at: datetime

class MembershipPagination(CustomBase):
    items: list[MembershipResponse]

class UpdateUserProject(CustomBase):
    category_id: Optional[int] = Field(default=None)

class UpdateMemberData(CustomBase):
    role: Update_Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
