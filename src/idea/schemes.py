from typing import Optional
from src.schemas import CustomBase

class IdeaCreateRequest(CustomBase):
    text: str

class IdeaResponse(CustomBase):
    id: int
    text: str
    owner_id: int
    theme_id: int
    project_id: int

class IdeaVoitesResponse(IdeaResponse):
    votes_count: int
    is_voted: Optional[bool] = False

class IdeaPagination(CustomBase):
    items: list[IdeaVoitesResponse]