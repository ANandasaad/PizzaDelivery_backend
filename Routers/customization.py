
from fastapi import APIRouter,status,Depends

from Schemas.customization import CustomizationPizzaListResponse,CustomizationPizzaResponse,CustomizationPizzaCreate,CustomizationPizzaUpdate
from Services.customization import getCustomizedOptions,createCustomization,getCustomizedOptionById,updateCustomizedOptionById,deletePizzaOptionById
from typing import Annotated
from sqlalchemy.orm import Session

from Database.db import get_db

db_dependency= Annotated[Session,Depends(get_db)]
customization_router=APIRouter(
    prefix="/customization",
    tags=["Customization"]
)
@customization_router.get("/", response_model=CustomizationPizzaListResponse, status_code=status.HTTP_200_OK)
async def get_customizations(db:db_dependency):
    return await getCustomizedOptions(db=db)
@customization_router.post("/", response_model=CustomizationPizzaResponse, status_code=status.HTTP_201_CREATED)
async def create_customization(request:CustomizationPizzaCreate, db:db_dependency):
    return await createCustomization(request=request,db=db)

@customization_router.get("/{id}", response_model=CustomizationPizzaResponse, status_code=status.HTTP_200_OK)
async def get_customizations(db:db_dependency,id:int):
    return await getCustomizedOptionById(db=db, id=id)

@customization_router.put("/{id}",response_model=CustomizationPizzaResponse, status_code=status.HTTP_200_OK)
async def update_customization(request:CustomizationPizzaUpdate,db:db_dependency,id:int):
    return await updateCustomizedOptionById(db=db, id=id, request=request)
@customization_router.delete("/{id}", response_model=CustomizationPizzaResponse, status_code=status.HTTP_200_OK)
async def delete_customization(db:db_dependency, id:int):
    return await deletePizzaOptionById(db=db, id=id)