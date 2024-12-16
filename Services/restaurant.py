from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from Models.models import User,Restaurant
from Schemas.restaurant import CreateRestaurant,FilterParams,SortByRating
from typing import Annotated
from config.O2Auth import get_current_user

from config.geolocation import get_location
from config.envFile import GOOGLE_MAPS_API_KEY

from Schemas.restaurant import UpdateRestaurant


async def createRestaurant(request: CreateRestaurant, db: Session,
                           current_user: Annotated[User, Depends(get_current_user)]):
    try:
        # Check if restaurant already exists
        restaurant = db.query(Restaurant).filter(Restaurant.name == request.name).first()
        if restaurant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already exists"
            )

        # Fetch geolocation (latitude, longitude) using Google Maps API
        response = await get_location(GOOGLE_MAPS_API_KEY, request.address)
        print(response)

        # Create a new restaurant entry
        new_restaurant = Restaurant(
            name=request.name,
            address=request.address,
            phone=request.phone,
            latitude=response["lat"],
            longitude=response["lng"],

        )
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)

        return {
            "message": "Restaurant created successfully",
            "data": new_restaurant
        }

    except HTTPException as e:
        # Handling specific HTTPException raised during geolocation fetch or other checks
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


async def getRestaurants(db:Session,filter:Annotated[FilterParams, Depends()], current_user: Annotated[User, Depends(get_current_user)]):
    try:

        restaurants = db.query(Restaurant)
        if filter.search:
            restaurants = restaurants.filter(Restaurant.name.ilike(f"%{filter.search}%"))

        #sort by rating
        if filter.sort:
            if filter.sort==SortByRating.ASC:
                restaurants = restaurants.order_by(Restaurant.rating.asc())
            else:
                restaurants = restaurants.order_by(Restaurant.rating.desc())

        # Get count of available
        count = restaurants.count()

        # Paginate restaurants
        restaurants = restaurants.offset(filter.offset).limit(filter.limit).all()
        if not restaurants:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurants not found"
            )

        return {
            "message": "Restaurants fetched successfully",
            "total": count,
            "limit": filter.limit,
            "offset": filter.offset,
            "data": restaurants
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def getRestaurant(id:int,db:Session, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        return {
            "message": "Restaurant fetched successfully",
            "data": restaurant
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def updateRestaurant(request:UpdateRestaurant,id:int,db:Session, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        # check is restaurant exists
        restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        # update the restaurant
        update_data={
            "rating": request.rating if request.rating else getattr(restaurant, "rating"),
            "name": request.name if request.name else getattr(restaurant, "name"),
            "address": request.address if request.address else getattr(restaurant, "address"),
            "phone": request.phone if request.phone else getattr(restaurant, "phone"),
            "latitude": request.latitude if request.latitude else getattr(restaurant, "latitude"),
            "longitude": request.longitude if request.longitude else getattr(restaurant, "longitude"),

        }

        db.query(Restaurant).filter(Restaurant.id == id).update(update_data)


        db.commit()
        db.refresh(restaurant)

        return {
            "message": "Restaurant updated successfully",
            "data": restaurant
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
