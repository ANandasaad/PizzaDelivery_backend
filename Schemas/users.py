from pydantic import BaseModel

from Models.models import UserRole


class UserBase(BaseModel):
    name: str | None = None
    email: str | None = None
    role: UserRole | None = None  # Assuming UserRole is an Enum
    is_active: bool | None = None
    address: str | None = None


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    address: str
    current_latitude: float
    current_longitude: float

    class Config:
        orm_mode = True

