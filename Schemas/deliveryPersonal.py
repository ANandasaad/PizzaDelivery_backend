from datetime import datetime

from pydantic import BaseModel


class DeliveryPersonal(BaseModel):
    name: str
    email: str
    password: str
    is_available: bool
    current_latitude: float
    current_longitude: float

class Response(DeliveryPersonal):
    id:int
    customer_order_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class DeliveryPersonalCreate(BaseModel):
    name: str
    email: str
    password: str
    is_available: bool
    customer_order_id: int


class DeliveryPersonalResponse(BaseModel):
    message: str
    data: Response