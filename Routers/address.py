from typing import Annotated

from fastapi import APIRouter, status, Depends

from Schemas.address import AddressResponse
from sqlalchemy.orm import Session
from Schemas.address import AddressCreate,UpdateAddress,SetAddress
from Database.db import get_db
from Models.models import User
from Services.address import createAddress,updateAddress,deleteAddress,setAddressDefault
from config.O2Auth import get_current_user


db_dependency= Annotated[Session,Depends(get_db)]
address_router = APIRouter(
    prefix="/address",
    tags=["Address"],

)

@address_router.post("/",response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(request:AddressCreate,db:db_dependency,current_user:Annotated[User, Depends(get_current_user)]):
    return await createAddress(request=request,db=db,current_user=current_user)

@address_router.patch("/{id}",response_model=AddressResponse, status_code=status.HTTP_200_OK)
async def update_address(id:int,request:UpdateAddress,db:db_dependency,current_user:Annotated[User, Depends(get_current_user)]):
    return await updateAddress(id=id,request=request,db=db, current_user=current_user)


@address_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(id:int,db:db_dependency,current_user:Annotated[User, Depends(get_current_user)]):
    return await deleteAddress(id=id,db=db, current_user=current_user)

@address_router.put("/{id}", response_model=AddressResponse, status_code=status.HTTP_200_OK)
async def set_address_default(id :int,request:SetAddress,db:db_dependency,current_user:Annotated[User, Depends(get_current_user)]):
    return await setAddressDefault(id=id,request=request,db=db, current_user=current_user)
