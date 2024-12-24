from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, status,Depends
from sqlalchemy.exc import IntegrityError
from config.hashing import hashPassword
from config.O2Auth import get_current_user
from Schemas.users import UserCreate,VerifyOTP,ResendOtp
from Models.models import User,Address,OtpRequest
from sqlalchemy.orm import Session
from Schemas.users import UserBase
import random
import time
from config.geolocation import get_location
from config.envFile import GOOGLE_MAPS_API_KEY
from utils.emailService import send_notification_otp


def generate_otp():

    return str(random.randint(10000, 99999))
async def register(user: UserCreate, db: Session):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Prepare address locations
    address_locations = []
    for address_data in user.addresses:
        # Fetch geolocation for the address
        response = await get_location(GOOGLE_MAPS_API_KEY, address_data.address)
        address_locations.append({
            "address": address_data.address,
            "latitude": response["lat"],
            "longitude": response["lng"],
            "is_primary": address_data.is_primary,
            "zipcode": address_data.zipcode,
        })

    # Hash the user's password
    hashed_password = hashPassword(user.password)
    #generate otp
    otp = generate_otp()

    # Create the new user instance
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        phone=user.phone,
    )
    db.add(new_user)

    try:
        # Commit the user to get their ID
        db.commit()
        db.refresh(new_user)

        # Add user addresses
        for address in address_locations:
            user_address = Address(
                user_id=new_user.id,
                address=address["address"],
                zipcode=address["zipcode"],
                latitude=address["latitude"],
                longitude=address["longitude"],
                is_primary=address["is_primary"]
            )
            db.add(user_address)

        # Add otp request
        expiration_time = datetime.utcnow() + timedelta(minutes=5)
        otp_request = OtpRequest(
            user_id=new_user.id,
            otp=otp,
            expires_time=expiration_time,
            attempts=0,
            lockout_time=None

        )
        db.add(otp_request)
        db.commit()

        # Final commit for all changes
        db.commit()
        db.refresh(new_user)
        await send_notification_otp(user.email,otp)

        return {
            "message":"User created successfully, Please Verify your Otp ",
            "data":new_user
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

def update(user:UserBase, db:Session, id:int, current_user:Annotated[User, Depends(get_current_user)]):
    if current_user.role !="customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    user_exists=db.query(User).filter(User.id==id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    update_data = {
        "name": user.name if user.name else getattr(user_exists, "name"),
        "email": user.email if user.email else getattr(user_exists, "email"),
        "role": user.role if user.role else getattr(user_exists , "role"),
    }
    db.query(User).filter(User.id == id).update(update_data)
    db.commit()
    db.refresh(user_exists)

    return user_exists


def get_all_users(db:Session,current_user:Annotated[User, Depends(get_current_user)]):

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    return db.query(User).all()

def getUserById(db:Session, id:int):
    user= db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
def deleteUserById(db:Session, id:int):
    user= db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {'user': user,
            "message": 'User deleted successfully'}

async def verifyUser(request:VerifyOTP,db:Session):
    try:
        # check is user exists

        user=db.query(User).filter(User.email==request.email).first()


        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        #check if user is already verified

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already verified"
            )

        otp_request=db.query(OtpRequest).filter(OtpRequest.user_id==user.id).first()


        if not otp_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Otp request not found"
            )
        if datetime.utcnow() > otp_request.expires_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired, resend the Otp request"
            )

        if otp_request.lockout_time and otp_request.lockout_time>datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="User is locked, please try again later"
            )

        #check if otp match or not
        if otp_request.otp!=request.otp:
            # increase attempts
            otp_request.attempts+=1
            db.commit()

            # check if max attempts is reached
            if otp_request.attempts>=3:
                # lockuser temporarily for 5 minutes
                otp_request.lockout_time=datetime.utcnow()+timedelta(minutes=5)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many attempts, please try again later"
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP"
            )


        otp_request.attempts=0
        otp_request.lockout_time=None
        user.is_verified=True
        db.commit()
        db.refresh(user)
        return {
            "message":"User verified successfully",
            "data":user
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(e)
        )



async  def resendOtp(request:ResendOtp, db:Session):
    try:
        user=db.query(User).filter(User.email==request.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already verified"
            )

        otp=generate_otp()
        otp_request=db.query(OtpRequest).filter(OtpRequest.user_id==user.id).first()
        if not otp_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Otp request not found"
            )
        otp_request.otp=otp
        otp_request.expires_time=datetime.utcnow()+timedelta(minutes=5)
        otp_request.attempts=0
        otp_request.lockout_time=None
        db.commit()
        db.refresh(otp_request)
        await send_notification_otp(user.email,otp)
        return {
            "message":"Otp resend successfully",
            "data":otp_request
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(e)
        )