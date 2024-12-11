from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from Models.models import User,Restaurant
from Schemas.restaurant import CreateRestaurant
from typing import Annotated
from config.O2Auth import get_current_user

from config.geolocation import get_location
from config.envFile import GOOGLE_MAPS_API_KEY


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