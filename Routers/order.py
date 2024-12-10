from typing import Annotated,List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Database.db import get_db

from Schemas.order import OrderCreate
from Services.order import createOrder,getOrders,getOrderById,updateOrderStatusById
from config.O2Auth import get_current_user
from Schemas.order import OrderResponse,OrderListResponse
from Models.models import OrderStatusByAdmin,User



order_router = APIRouter(
    prefix="/order",
    tags=["Order"]
)
db_dependency= Annotated[Session,Depends(get_db)]
@order_router.post("/",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def create_order(request:OrderCreate,db:db_dependency, current_user: Annotated[User, Depends(get_current_user)]):
    return await createOrder(request=request,db=db, current_user=current_user)

@order_router.get("/",response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_orders(db:db_dependency):
    return await getOrders(db=db)

@order_router.get("/{id}",response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(id:int,db:db_dependency):
    return await getOrderById(db=db,id=id)

@order_router.put("/{id}",response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def order_status_by_admin(id:int,db:db_dependency,request:OrderStatusByAdmin):
    return await updateOrderStatusById(db=db,id=id,request=request)

