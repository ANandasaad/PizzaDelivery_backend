from fastapi import APIRouter, Depends,status,Request
from typing import Annotated

from sqlalchemy.orm import Session

from Database.db import get_db


from Services.payment import verifyPayment


payment_router=APIRouter(
    prefix="/payment",
    tags=["Payment"]
)
db_dependency= Annotated[Session,Depends(get_db)]
@payment_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_payment(request:Request,db:db_dependency):
    return await verifyPayment(request=request,db=db)
