from typing import Optional
from pydantic import Field

from src.schemas import CustomBase
from src.project.schemes import ProjectResponse

class CategoryCreate(CustomBase):
    name: str= Field(max_length=30) 
    color: str = Field() 

class CategoryUpdate(CustomBase):
    name: Optional[str] = Field(default=None, max_length=30) 
    color: Optional[str] = Field(default=None) 

class CategoryResponse(CategoryCreate):
    id: int
    user_id: int

class CategoryBase(CustomBase):
    id: int
    name: str
    color: str
    user_id: int

class CategoryWithProjectsResponse(CategoryBase):
    projects: list[ProjectResponse] = []

class CategoryPagination(CustomBase):
    categories: list[CategoryWithProjectsResponse]
    projects: list[ProjectResponse]
    