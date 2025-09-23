from src.models import CustomBase
from pydantic import Field
from src.config import settings

class InviteModel(CustomBase):
    email: str
    role: str = Field(default=settings.DEFAULT_PROJECT_ROLE)

class InviteProjectData(CustomBase):
    user_id: int
    role: str = Field(default=settings.DEFAULT_PROJECT_ROLE)
    project_id: int