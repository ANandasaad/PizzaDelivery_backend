from Schemas.pizza import PizzaOptionCreate, PizzaOptionUpdate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Models.models import PizzaOption,Menu

from Schemas.pizza import FilterParams,SortOrder




async def createPizzaOption(request: PizzaOptionCreate, db: Session):
    try:
       # Check if menu exists
        menu_exists = db.query(Menu).filter(Menu.id == request.menu_id).first()
        if not menu_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu not found"
            )
        # Check if option already exists
        option = db.query(PizzaOption).filter(PizzaOption.name == request.name).first()
        if option:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pizza Option already exists"
            )

        # Create a new option
        new_option = PizzaOption(name=request.name, description=request.description, base_price=request.base_price, menu_id=request.menu_id,type=request.type, image_url=request.image_url)
        db.add(new_option)
        db.commit()
        db.refresh(new_option)

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Pizza Option created successfully",
            "data": new_option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def updatePizzaById(request:PizzaOptionUpdate, db: Session, id:int):
    try:
        # Check if option exists
        option = db.query(PizzaOption).filter(PizzaOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza Option not found"
            )

        # Update the option
        update_data={
            "name": request.name if request.name else getattr(option, "name"),
            "description": request.description if request.description else getattr(option, "description"),
            "base_price": request.base_price if request.base_price else getattr(option, "base_price"),
            "type": request.type if request.type else getattr(option, "type"),
            "image_url": request.image_url if request.image_url else getattr(option, "image_url"),
        }

        db.query(PizzaOption).filter(PizzaOption.id == id).update(update_data)

        db.commit()
        db.refresh(option)


        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Pizza Option updated successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def getPizzaOptionById(id:int, db:Session):
    try:
        # Check if option exists
        option = db.query(PizzaOption).filter(PizzaOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza Option not found"
            )

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Pizza Option fetched successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def getAllPizzaOptions(db:Session,filter:FilterParams):
    try:
        # check if options exist

        options = db.query(PizzaOption)
        if filter.search:
            options = options.filter(PizzaOption.name.ilike(f"%{filter.search}%"))
        if filter.type:
            options = options.filter(PizzaOption.type == filter.type.value)

       #sort by price
        if filter.sort:
            if filter.sort==SortOrder.ASC:
                options = options.order_by(PizzaOption.base_price.asc())
            else:
                options = options.order_by(PizzaOption.base_price.desc())


        # Get count of available
        count = options.count()

        # Paginate options
        options = options.offset(filter.offset).limit(filter.limit).all()
        if not options:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza Options not found"
            )

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Pizza Options fetched successfully",
            "total": count,
            "limit": filter.limit,
            "offset": filter.offset,
            "data": options
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def deletePizzaOptionById(id:int, db:Session):
    try:
        # Check if option exists
        option = db.query(PizzaOption).filter(PizzaOption.id == id).first()
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza Option not found"
            )

        # Delete the option
        db.delete(option)
        db.commit()
        return {
            "message": "Pizza Option deleted successfully",
            "data": option
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )