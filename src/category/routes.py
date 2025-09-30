from fastapi import APIRouter, status, Depends


from src.database import DbSession
from src.user.dependencies import CurrentUser
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
    categories = await CategoryService(session).get_categories(user.id)
    return {
        "items": categories
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

@category_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    session: DbSession,
    user: CurrentUser,
    category_id: int
):
    await CategoryService(session).delete_category(category_id, user.id)
