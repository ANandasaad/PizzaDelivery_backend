from Schemas.auth import Login
from Models.models import User
from fastapi import HTTPException, status,Depends
from pydantic import constr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.hashing import verifyPassword,createToken
from fastapi.security import  OAuth2PasswordRequestForm
import logging
from sqlalchemy.sql.annotation import Annotated


async def loginUser(db:Session,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    try:
        # check is user exists

        user=db.query(User).filter(User.email==form_data.username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        # check password
        if not verifyPassword(form_data.password,user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        #if user is not verified

        if not user.is_verified:
            logging.error("User %s is not verified.", form_data.username)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is not verified. Please check your email for verification instructions."
            )
        # create token
        data = {'email': user.email, 'id': user.id, 'role':user.role}
        token = createToken(data)
        return {'access_token': token, "token_type": "bearer"}




    except IntegrityError:

        db.rollback()

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="An unexpected error occurred. Please try again."

        )
