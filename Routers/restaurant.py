from fastapi import APIRouter, Depends,status
from typing import Annotated

from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.restaurant import RestaurantResponse,CreateRestaurant
from Services.restaurant import createRestaurant
from Models.models import User
from config.O2Auth import get_current_user

db_dependency= Annotated[Session,Depends(get_db)]

restaurant_router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)

@restaurant_router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(request:CreateRestaurant, db:db_dependency, current_user:Annotated[User,Depends(get_current_user)]):
    return await createRestaurant(request=request,db=db, current_user=current_user)