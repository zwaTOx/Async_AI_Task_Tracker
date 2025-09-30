from typing import Optional
from pydantic import Field

from src.models import CustomBase


class CategoryCreate(CustomBase):
    name: str= Field(max_length=30) 
    color: str = Field(max_length=10) 

class CategoryUpdate(CustomBase):
    name: Optional[str] = Field(default=None, max_length=30) 
    color: Optional[str] = Field(default=None, max_length=10) 

class CategoryResponse(CategoryCreate):
    id: int
    user_id: int

class CategoryPagination(CustomBase):
    items: list[CategoryResponse]