from typing import Optional
from sqlmodel import Field

from src.models import CustomBase


class ProjectBase(CustomBase):
    name: str = Field('Project', max_length=100, min_length=5)
    description: str = Field('Description',  max_length=300)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    icon_id: Optional[int] = Field(None)

class ProjectResponse(CustomBase):
    id: int
    owner_id: int
    name: str
    description: str
    
class ProjectPagination(CustomBase):
    items: list[ProjectResponse]