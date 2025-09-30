from pydantic import Field

from src.models import CustomBase


class CategoryCreate(CustomBase):
    name: str= Field(max_length=15) 
    color: str = Field(max_length=5) 

class CategoryResponse(CategoryCreate):
    user_id: int

class CategoryPagination(CustomBase):
    items: list[CategoryResponse]