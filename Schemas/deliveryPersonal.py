from datetime import datetime

from pydantic import BaseModel


class DeliveryPersonal(BaseModel):
    name: str
    email: str
    password: str
    is_available: bool
    current_latitude: float
    current_longitude: float
    address: str

class Response(DeliveryPersonal):
    id:int

    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class DeliveryPersonalCreate(BaseModel):
    name: str
    email: str
    password: str
    is_available: bool
    address: str



class DeliveryPersonalResponse(BaseModel):
    message: str
    data: Response