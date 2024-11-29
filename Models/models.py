import enum
from Database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum
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
