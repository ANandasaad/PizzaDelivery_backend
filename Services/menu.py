from Schemas.menu import PizzaMenu
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from Models.models import Menu

def createMenu(request: PizzaMenu, db: Session):
    try:
        # Check if menu already exists
        menu = db.query(Menu).filter(Menu.name == request.name).first()
        if menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu already exists"
            )

        # Create a new menu
        new_menu = Menu(name=request.name, description=request.description)
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)

        # Convert SQLAlchemy object to dictionary or Pydantic model
        return {
            "message": "Menu created successfully",
            "data": new_menu
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
def getMenus(db:Session):
    try:
        menus= db.query(Menu).all()
        if not menus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No menus found"
            )
        return {
            "message": "Menus fetched successfully",
            "data": menus
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


def getMenuById(db:Session, id:int):
    try:
        menu= db.query(Menu).filter(Menu.id == id).first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu not found"
            )
        return {
            "message": "Menu fetched successfully",
            "data": menu
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

