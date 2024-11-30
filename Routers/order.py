from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.order import OrderCreate
from Services.order import createOrder

order_router = APIRouter(
    prefix="/order",
    tags=["Order"]
)
db_dependency= Annotated[Session,Depends(get_db)]
@order_router.post("/",status_code=status.HTTP_201_CREATED)
async def create_order(request:OrderCreate,db:db_dependency):
    return await createOrder(request=request,db=db)