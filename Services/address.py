
from Schemas.address import AddressCreate,UpdateAddress,SetAddress
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Models.models import User,Address
from typing import Annotated
from fastapi import Depends, HTTPException,status
from config.O2Auth import get_current_user
from utils.helper import  is_within_delivery_radius
from config.validateAddress import validate_address



async def createAddress(request:AddressCreate,db:Session,current_user:Annotated[User, Depends(get_current_user)]):

    try:
        # get user id from current user
        user_id = current_user.id
        # check if user already exists
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        # validate the address

        formatted_address, latitude, longitude = await validate_address(request.address, request.locality)

        if not formatted_address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid address"
            )

        # Validate delivery address radius
        if not await is_within_delivery_radius(latitude, longitude,delivery_radius=20.0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address is outside the delivery radius"
            )


        #check max address limit
        user_address_count = db.query(Address).filter(Address.user_id == user_id).count()

        if  user_address_count>=5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum address limit reached"
            )

        #create a new address
        new_address = Address(
            user_id=user_id,
            address=formatted_address,
            city=request.city,
            state=request.state,
            locality=request.locality,
            additional_instructions=request.additional_instructions,
            is_primary=request.is_primary,
            zipcode=request.zipcode,
            latitude=latitude,
            longitude=longitude
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return {
            "message": "Address created successfully",
            "data": new_address
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



async def updateAddress(id:int, request:UpdateAddress,db:Session,current_user:Annotated[User, Depends(get_current_user)]):
    try:
        # check if user is role is customer or not
        current_user_role = current_user.role
        if current_user_role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customer can update address"
            )
        # get address from db
        address = db.query(Address).filter(Address.id == id).first()
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        # check if requested body is existing or not


        # update address
        update_data = {
            "address": request.address if request.address else getattr(address,"address"),
            "city": request.city if request.city else getattr(address,"city"),
            "state": request.state if request.state else getattr(address,"state"),
            "locality": request.locality if request.locality else getattr(address,"locality"),
            "additional_instructions": request.additional_instructions if request.additional_instructions else getattr(address,"additional_instructions"),
            "is_primary": request.is_primary if request.is_primary else getattr(address,"is_primary"),
            "zipcode": request.zipcode if request.zipcode else getattr(address,"zipcode"),

        }
        db.query(Address).filter(Address.id == id).update(update_data)
        db.commit()
        db.refresh(address)
        return {
            "message": "Address updated successfully",
            "data": address
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def deleteAddress(id:int,db:Session,current_user:Annotated[User, Depends(get_current_user)]):
    try:
        # check if user is role is customer or not
        current_user_role = current_user.role
        if current_user_role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customer can delete address"
            )
        #check that user id is exits in address is equal to current user id
        address=db.query(Address).filter(Address.user_id==current_user.id, Address.id==id).first()

        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found or you do not have permission to edit it"
            )
        db.delete(address)
        db.commit()
        return {
            "message": "Address deleted successfully"
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def setAddressDefault(id:int, request:SetAddress,db:Session,current_user:Annotated[User, Depends(get_current_user)]):
    try:

        user_address= db.query(Address).filter(Address.user_id==current_user.id).all()

        if len(user_address)==0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user should have at least one address"
            )

        for address in user_address:
            address.is_primary=False

        address=db.query(Address).filter(Address.id==id, Address.user_id==current_user.id).first()
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found or you do not have permission to edit it"
            )

        address.is_primary=request.is_primary
        # update is_primary in address

        db.commit()
        db.refresh(address)
        return {
            "message": "Address set as default successfully",
            "data": address
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



