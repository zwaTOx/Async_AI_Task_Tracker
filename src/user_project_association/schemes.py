from datetime import datetime
from src.models import CustomBase
from pydantic import Field
from fastapi import Query
from .utils import Roles
from src.config import settings

class InviteModel(CustomBase):
    email: str = Query(...)
    role: Roles = Query(default=settings.DEFAULT_PROJECT_ROLE)

class InviteProjectData(CustomBase):
    user_id: int
    role: Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
    project_id: int

class MembershipResponse(CustomBase):
    user_id: int
    project_id: int
    role: Roles
    joined_at: datetime

class UpdateMemberData(CustomBase):
    role: Roles = Field(default=settings.DEFAULT_PROJECT_ROLE)
