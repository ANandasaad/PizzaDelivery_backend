from pydantic import BaseModel
from typing import List

from Schemas.menu import PizzaMenu


class Restaurant(BaseModel):
    name: str
    address: str
    phone: str
    latitude: float
    longitude: float

class CreateRestaurant(Restaurant):
    class Config:
        orm_mode = True

class Response(Restaurant):

    id: int
    menus: List[PizzaMenu]
    class Config:
        orm_mode = True

class RestaurantResponse(BaseModel):
    message: str
    data: Response

