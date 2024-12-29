
from fastapi import APIRouter, Depends, status
from typing import Annotated
from Models.models import User
from sqlalchemy.orm import Session

from Database.db import get_db
from config.O2Auth import get_current_user
from Schemas.category import CategoryResponse,CategoryCreate,CategoryUpdate,CategoryListResponse
from Services.category import createCategory,getAllCategories,updateCategoryById,getCategoryById,deleteCategoryById

category_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)
db_dependency= Annotated[Session,Depends(get_db)]


@category_router.post("/",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
async def create_category(category:CategoryCreate,db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await createCategory(db=db,category=category)

@category_router.get("/",response_model=CategoryListResponse,status_code=status.HTTP_200_OK,)
async def get_categories(db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await getAllCategories(db=db)

@category_router.get("/{category_id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
async def get_category(category_id:int,db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await getCategoryById(db=db,category_id=category_id)

@category_router.put("/{category_id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
async def update_category(category_id:int,category:CategoryUpdate,db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await updateCategoryById(db=db,category_id=category_id,category=category)

@category_router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id:int,db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await deleteCategoryById(db=db,category_id=category_id)