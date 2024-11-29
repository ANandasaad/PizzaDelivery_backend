from pydantic import BaseModel
from typing import List

from Schemas.pizza import PizzaResult


class PizzaMenu(BaseModel):
    name: str
    description: str | None = None


class Return(PizzaMenu):
    id: int
    pizzas:List[PizzaResult]

class PizzaMenuResponse(BaseModel):
    message: str
    data: Return

class PizzaMenuListResponse(BaseModel):
    message: str
    data: List[Return]
