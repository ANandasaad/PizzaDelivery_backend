import enum
from Database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum,Text,ForeignKey,Float
from sqlalchemy.orm import relationship
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    DELIVERY = "deliver"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = Column(Boolean, nullable=False, default=True)

class CustomizationType(str,enum.Enum):
    SIZE = "size"
    TOPPING = "topping"
    CRUST = "crust"
class PizzaType(str,enum.Enum):
    VEG = "veg"
    NONVEG= "non-veg"
class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique=True, nullable=False)
    description = Column(Text, nullable=True)
    pizzas = relationship("PizzaOption", back_populates="menu")

class PizzaOption(Base):
    __tablename__ = "pizza_options"
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    name = Column(String, unique=True,nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(PizzaType), nullable=False, default=PizzaType.VEG)
    image_url=Column(String, nullable=True)
    base_price = Column(Float, nullable=False)
    menu= relationship("Menu", back_populates="pizzas")
    customizations= relationship("CustomizationOption", back_populates="pizza_option")

class CustomizationOption(Base):
    __tablename__="customization"
    id = Column(Integer, primary_key=True, index=True)
    pizza_option_id = Column(Integer, ForeignKey("pizza_options.id"))
    type = Column(Enum(CustomizationType), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    pizza_option = relationship("PizzaOption", back_populates="customizations")


