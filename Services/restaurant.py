from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from Models.models import User,Restaurant
from Schemas.restaurant import CreateRestaurant
from typing import Annotated
from config.O2Auth import get_current_user

from config.geolocation import get_location

GOOGLE_MAPS_API_KEY ="AIzaSyBbom_9El8YWDyHeq0zp-rWRX_1QZJTkWI"
async def createRestaurant(request:CreateRestaurant, db:Session, current_user:Annotated[User, Depends(get_current_user)]):
    try:
        # fectch longitude and latitude

        response = await get_location(GOOGLE_MAPS_API_KEY)
        print(response)
        # create a new restaurant
        new_restaurant = Restaurant(
            name=request.name,
            address=request.address,
            phone=request.phone,
            latitude=response["location"]["lat"],
            longitude=response["location"]["lng"],
        )
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
        return {
            "message": "Restaurant created successfully",
            "data": new_restaurant
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

