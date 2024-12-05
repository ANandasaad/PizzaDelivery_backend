from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.deliveryPersonal import DeliveryPersonalCreate, DeliveryPersonalResponse
from Services.deliveryPersonal import createDeliveryPersonal
deliveryPersonal_router = APIRouter(
    prefix="/deliveryPersonal",
    tags=["Delivery Personal"]
)
db_dependency= Annotated[Session,Depends(get_db)]

@deliveryPersonal_router.post("/", response_model=DeliveryPersonalResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery_personal(request:DeliveryPersonalCreate, db:db_dependency):
    return await createDeliveryPersonal(request=request,db=db)