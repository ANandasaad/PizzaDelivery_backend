import enum
from Database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, ForeignKey, Float, DateTime,func
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
    orders = relationship("Order", back_populates="customer")

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
    order_items = relationship("OrderItem", back_populates="pizza_option")

class CustomizationOption(Base):
    __tablename__="customization"
    id = Column(Integer, primary_key=True, index=True)
    pizza_option_id = Column(Integer, ForeignKey("pizza_options.id"))
    type = Column(Enum(CustomizationType), nullable=False)
    name = Column(String,unique=True, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    pizza_option = relationship("PizzaOption", back_populates="customizations")
    selected_customizations = relationship("SelectedCustomization", back_populates="customization")

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    total_price = Column(Float, nullable=False)
    customer = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    created_at = Column(DateTime,default=func.now(), nullable=False)
    updated_at = Column(DateTime,default=func.now(), nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id",ondelete="CASCADE"), nullable=False)
    pizza_option_id = Column(Integer, ForeignKey("pizza_options.id"))
    quantity = Column(Integer, nullable=False)
    pizza_option = relationship("PizzaOption", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
    price = Column(Integer, nullable=False)
    selected_customizations = relationship("SelectedCustomization", back_populates="order_item", cascade="all, delete")
    created_at = Column(DateTime,default=func.now(), nullable=False)
    updated_at = Column(DateTime,default=func.now(), nullable=False)

class SelectedCustomization(Base):
    __tablename__ = "selected_customizations"
    id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"))
    customization_id = Column(Integer, ForeignKey("customization.id"))
    customization_price=Column(Float, nullable=False)
    order_item = relationship("OrderItem", back_populates="selected_customizations")
    customization = relationship("CustomizationOption", back_populates="selected_customizations")

    