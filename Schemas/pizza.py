from pydantic import BaseModel

from Models.models import PizzaType
from typing import List


class PizzaOption(BaseModel):
    name: str
    description: str | None = None
    type: PizzaType
    image_url: str | None = None
    base_price: float
    menu_id: int

class PizzaOptionCreate(PizzaOption):
    pass

class PizzaResult(PizzaOption):
    id: int
    class Config:
        orm_mode = True
class PizzaOptionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    type: PizzaType | None = None
    image_url: str | None = None
    base_price: float | None = None
class PizzaOptionResponse(BaseModel):
    message: str
    data: PizzaResult
class PizzaOptionListResponse(BaseModel):
    message: str
    data: List[PizzaResult]

