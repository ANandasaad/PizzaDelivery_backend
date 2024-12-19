from pydantic import BaseModel, EmailStr, Field
from typing import List

from Models.models import UserRole

class AddressCreate(BaseModel):
    address: str
    latitude: float | None = None
    longitude: float | None = None
    is_primary: bool

    class Config:
        orm_mode = True
class UserBase(BaseModel):
    name: str | None = None
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10, pattern=r"^[7-9]\d{9}$")
    role: UserRole | None = None  # Assuming UserRole is an Enum
    is_active: bool | None = None
    addresses: List[AddressCreate]


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

