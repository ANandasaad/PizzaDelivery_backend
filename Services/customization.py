from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from Models.models import CustomizationOption
from Schemas.customization import CustomizationPizzaCreate,CustomizationPizzaUpdate


async def getCustomizedOptions(db:Session):
    # Get the default
    try:
        query = db.query(CustomizationOption).all()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customizations not found"
            )
        return {
            "message": "Customization fetched successfully",
            "data": query
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


async def createCustomization(request:CustomizationPizzaCreate, db:Session):

    try:
        # Check if name is already
        option = db.query(CustomizationOption).filter(CustomizationOption.name == request.name).first()
        if option:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customization already exists"
            )
        # Create a new option
        new_option = CustomizationOption(name=request.name, price=request.price, type=request.type, pizza_option_id=request.pizza_option_id)
        db.add(new_option)
        db.commit()
        db.refresh(new_option)

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Customization created successfully",
            "data": new_option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def getCustomizedOptionById(db:Session, id:int):
    try:
        # Check if option exists
        option = db.query(CustomizationOption).filter(CustomizationOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customization not found"
            )

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Customization fetched successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def updateCustomizedOptionById(db:Session, id:int, request:CustomizationPizzaUpdate):
    try:
        # Check if option exists
        option = db.query(CustomizationOption).filter(CustomizationOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customization not found"
            )

        # Update the option
        update_data={
            "name": request.name if request.name else getattr(option, "name"),
            "price": request.price if request.price else getattr(option, "price"),
            "type": request.type if request.type else getattr(option, "type"),

        }

        db.query(CustomizationOption).filter(CustomizationOption.id == id).update(update_data)

        db.commit()
        db.refresh(option)

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Customization updated successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


async def deletePizzaOptionById(db:Session, id:int):
    try:
        # Check if option exists
        option = db.query(CustomizationOption).filter(CustomizationOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customization not found"
            )

        # Delete the option
        db.delete(option)
        db.commit()
        return {
            "message": "Customization deleted successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )