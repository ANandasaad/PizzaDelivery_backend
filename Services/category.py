from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Schemas.category import CategoryResponse,CategoryCreate,CategoryUpdate,CategoryListResponse
from Models.models import Categories
from fastapi import HTTPException,status



async def createCategory(db:Session,category:CategoryCreate):
    try:
        #check if category is already exists
        category_exists=db.query(Categories).filter(Categories.name==category.name).first()
        if category_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists"
            )
        #create a new category
        new_category=Categories(name=category.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        #convert sqlalchemy object to dictionary or pydantic model
        return {
            "message":"Category created successfully",
            "data":new_category
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def getAllCategories(db:Session):
    try:
        # get all categories
        categories=db.query(Categories).all()
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categories not found"
            )
        #convert sqlalchemy object to dictionary or pydantic model
        return {
            "message":"Categories fetched successfully",
            "data":categories
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


async def getCategoryById(category_id:int,db:Session):
    try:
        # get category by id
        category=db.query(Categories).filter(Categories.id==category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        #convert sqlalchemy object to dictionary or pydantic model
        return {
            "message":"Category fetched successfully",
            "data":category
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def updateCategoryById(category_id:int,request:CategoryUpdate,db:Session):
    try:
        # get category by id
        category=db.query(Categories).filter(Categories.id==category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        #update category
        category.name=request.name
        db.commit()
        db.refresh(category)

        #convert sqlalchemy object to dictionary or pydantic model
        return {
            "message":"Category updated successfully",
            "data":category
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def deleteCategoryById(category_id:int,db:Session):
    try:
        # get category by id
        category=db.query(Categories).filter(Categories.id==category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        #delete category
        db.delete(category)
        db.commit()

        #convert sqlalchemy object to dictionary or pydantic model
        return {
            "message":"Category deleted successfully",
            "data":category
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
