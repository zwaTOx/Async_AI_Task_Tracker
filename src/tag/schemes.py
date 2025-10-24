from typing import Optional
from src.schemas import CustomBase

class TagCreate(CustomBase):
    name: str
    description: Optional[str]
    color: str

class TagUpdate(CustomBase):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    
class TagResponse(TagCreate):
    id: int

class TagPargination(CustomBase):
    items: list[TagResponse]