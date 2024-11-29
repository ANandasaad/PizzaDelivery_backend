
from fastapi import APIRouter, status,HTTPException, Depends
from typing import Annotated, List
from Schemas.menu import PizzaMenu,PizzaMenuResponse,PizzaMenuListResponse

from Database.db import get_db
from Services.menu import createMenu,getMenus,getMenuById
from sqlalchemy.orm import Session

menu_router = APIRouter(

    tags=["Menu"]
)
db_dependency= Annotated[Session,Depends(get_db)]
@menu_router.post("/create-menu", response_model=PizzaMenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(request:PizzaMenu, db:db_dependency):
    return createMenu(request=request,db=db)

@menu_router.get("/get-menus", response_model=PizzaMenuListResponse, status_code=status.HTTP_200_OK)
def get_menus(db:db_dependency):
    return getMenus(db=db)
@menu_router.get("/get-menu/{id}", response_model=PizzaMenuResponse, status_code=status.HTTP_200_OK)
def get_menu(id:int, db:db_dependency):
    return getMenuById(db=db, id=id)