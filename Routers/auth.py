from typing import Annotated

from fastapi import APIRouter, status, Depends
from Services.auth import loginUser
from Schemas.auth import Login
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from Database.db import get_db

from Schemas.auth import Token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

db_dependency= Annotated[Session,Depends(get_db)]
@auth_router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login(db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await loginUser(db=db,form_data=form_data)