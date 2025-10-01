from fastapi import APIRouter, status, Depends


from src.database import DbSession
from src.user.dependencies import CurrentUser
from src.user_project_association.dependencies import verify_project_member
from .service import CategoryService
from .schemes import CategoryCreate, CategoryResponse, CategoryPagination, CategoryUpdate

category_router = APIRouter()

@category_router.get(
    "",
    response_model=CategoryPagination
)
async def get_categories(
    session: DbSession,
    user: CurrentUser
):
    categories, projects = await CategoryService(session).get_categories(user.id)
    return {
            "categories": categories,
            "projects": projects
        }

@category_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse
)
async def create_category(
    session: DbSession,
    user: CurrentUser,
    category_data: CategoryCreate
):
    new_category = await CategoryService(session).create_category(user.id, category_data)
    return new_category

@category_router.patch(
    "/{category_id}",
)
async def update_category(
    session: DbSession,
    user: CurrentUser,
    category_id: int,
    category_update: CategoryUpdate
):
    updated_category = await CategoryService(session).update_category(user.id, category_id, category_update)
    return updated_category

@category_router.post(
    "/{category_id}/projects/{project_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_project_member)],
    response_model=CategoryResponse  
)
async def add_project_to_category(
    session: DbSession,
    user: CurrentUser,
    category_id: int,
    project_id: int
):
    result = await CategoryService(session).add_project_to_category(
        user_id=user.id,
        category_id=category_id,
        project_id=project_id
    )
    return result