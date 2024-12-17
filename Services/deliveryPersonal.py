from idlelib.rpc import response_queue

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Schemas.deliveryPersonal import DeliveryPersonalCreate
from Models.models import DeliveryPersonal

from config.hashing import hashPassword

from config.envFile import GOOGLE_MAPS_API_KEY

from config.geolocation import get_location


async def createDeliveryPersonal(request:DeliveryPersonalCreate,db:Session):
    try:
        # check email deliverPersonal exits
        deliveryPersonal = db.query(DeliveryPersonal).filter(DeliveryPersonal.email == request.email).first()
        if deliveryPersonal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery Personal already exists"
            )
        response = await get_location(GOOGLE_MAPS_API_KEY, request.address)
        hashedPassword=hashPassword(request.password)
        deliveryPersonal = DeliveryPersonal(email=request.email,name=request.name,password=hashedPassword,address=request.address,current_latitude=response["lat"],current_longitude=response["lng"])
        db.add(deliveryPersonal)
        db.commit()
        db.refresh(deliveryPersonal)
        return {
            "message": "Delivery Personal created successfully",
            "data": deliveryPersonal
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )