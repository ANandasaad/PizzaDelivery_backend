from fastapi import APIRouter, Depends,status
from typing import Annotated

from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.restaurant import RestaurantResponse,CreateRestaurant,RestaurantListResponse,FilterParams,UpdateRestaurant
from Services.restaurant import createRestaurant,getRestaurants,getRestaurant,updateRestaurant
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

@restaurant_router.get("/",response_model=RestaurantListResponse,status_code=status.HTTP_200_OK)
async def get_restaurants(db:db_dependency,filter:Annotated[FilterParams, Depends()], current_user:Annotated[User,Depends(get_current_user)]):
    return await getRestaurants(db=db,filter=filter, current_user=current_user)

@restaurant_router.get("/{id}",response_model=RestaurantResponse,status_code=status.HTTP_200_OK)
async def get_restaurant(id:int,db:db_dependency, current_user:Annotated[User,Depends(get_current_user)]):
    return await getRestaurant(id=id,db=db,current_user=current_user)
@restaurant_router.put("/{id}", response_model=RestaurantResponse,status_code=status.HTTP_200_OK)
async def update_restaurant(request:UpdateRestaurant,id:int,db:db_dependency,current_user:Annotated[User,Depends(get_current_user)]):
    return await updateRestaurant(request=request,db=db,id=id, current_user=current_user)