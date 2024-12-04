from typing import Annotated,List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.order import OrderCreate
from Services.order import createOrder,getOrders,getOrderById

from Schemas.order import OrderResponse,OrderListResponse



order_router = APIRouter(
    prefix="/order",
    tags=["Order"]
)
db_dependency= Annotated[Session,Depends(get_db)]
@order_router.post("/",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def create_order(request:OrderCreate,db:db_dependency):
    return await createOrder(request=request,db=db)

@order_router.get("/",response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_orders(db:db_dependency):
    return await getOrders(db=db)

@order_router.get("/{id}",response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(id:int,db:db_dependency):
    return await getOrderById(db=db,id=id)

