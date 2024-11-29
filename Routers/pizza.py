

from fastapi import APIRouter, Depends, status
from typing import Annotated
from Schemas.pizza import PizzaOptionResponse,PizzaOptionCreate,PizzaOptionUpdate,PizzaOptionListResponse
from sqlalchemy.orm import Session
from Services.pizza import createPizzaOption,updatePizzaById,getPizzaOptionById,getAllPizzaOptions,deletePizzaOptionById
from Database.db import get_db


db_dependency= Annotated[Session,Depends(get_db)]
pizza_router = APIRouter(
    prefix="/pizza",
    tags=["Pizza"]
)

@pizza_router.post("/", response_model=PizzaOptionResponse, status_code=status.HTTP_201_CREATED)
async def create_pizza_option(request: PizzaOptionCreate, db:db_dependency):
    return await createPizzaOption(request=request, db=db)


@pizza_router.put("/{id}", response_model=PizzaOptionResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_pizza_option(request: PizzaOptionUpdate, db:db_dependency, id:int):
    return await updatePizzaById(request=request, db=db, id=id)

@pizza_router.get("/{id}", response_model=PizzaOptionResponse, status_code=status.HTTP_200_OK)
async def get_pizza_option(id:int, db:db_dependency):
    return await getPizzaOptionById(id=id, db=db)

@pizza_router.get("/", response_model=PizzaOptionListResponse, status_code=status.HTTP_200_OK)
async def get_pizza_options(db:db_dependency):
    return await getAllPizzaOptions(db=db)

@pizza_router.delete("/{id}", response_model=PizzaOptionResponse, status_code=status.HTTP_200_OK)
async def delete_pizza_option(db:db_dependency, id:int):
    return await deletePizzaOptionById(db=db, id=id)