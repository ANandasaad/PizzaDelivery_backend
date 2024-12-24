from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Database.db import get_db
from Schemas.users import UserCreate, UserResponse,UserRegisterResponse
from Services.user import register,update,get_all_users,getUserById,deleteUserById,verifyUser,resendOtp

from Schemas.users import UserBase,VerifyOTP,ResendOtp
from config.O2Auth import get_current_user
from Models.models import User

db_dependency= Annotated[Session,Depends(get_db)]
user_router=APIRouter(

    tags=['Users']
)

@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(request:UserCreate, db:db_dependency):
     return await register(user=request,db=db)
@user_router.put("/update/{id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
def update_user(request:UserBase, db:db_dependency, id:int, current_user:Annotated[User, Depends(get_current_user)]):
    return update(user=request,db=db,id=id, current_user=current_user)

@user_router.get("/get-all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all(db:db_dependency,current_user:Annotated[User, Depends(get_current_user)]):

    return get_all_users(db=db,current_user=current_user)

@user_router.get("/get-user/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(id:int, db:db_dependency):
    return getUserById(db=db,id=id)
@user_router.delete("/delete-user/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(db:db_dependency, id:int):
    return deleteUserById(db=db,id=id)
@user_router.put("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(request:VerifyOTP, db:db_dependency):
    return await verifyUser(request=request,db=db)
@user_router.put("/resend_otp", status_code=status.HTTP_200_OK)
async def resend_otp(request:ResendOtp, db:db_dependency):
    return await resendOtp(request=request,db=db)