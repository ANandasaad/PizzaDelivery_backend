from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Schemas.deliveryPersonal import DeliveryPersonalCreate
from Models.models import DeliveryPersonal

from config.hashing import hashPassword


async def createDeliveryPersonal(request:DeliveryPersonalCreate,db:Session):
    try:
        # check email deliverPersonal exits
        deliveryPersonal = db.query(DeliveryPersonal).filter(DeliveryPersonal.email == request.email).first()
        if deliveryPersonal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery Personal already exists"
            )
        hashedPassword=hashPassword(request.password)
        deliveryPersonal = DeliveryPersonal(email=request.email,name=request.name,password=hashedPassword,customer_order_id=request.customer_order_id)
        db.add(deliveryPersonal)
        db.commit()
        db.refresh(deliveryPersonal)
        return {
            "message": "Delivery Personal created successfully",
            "data": deliveryPersonal
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )