from pydantic import BaseModel
from typing import List

class PizzaMenu(BaseModel):
    name: str
    description: str | None = None


class Return(PizzaMenu):
    id: int

class PizzaMenuResponse(BaseModel):
    message: str
    data: Return

class PizzaMenuListResponse(BaseModel):
    message: str
    data: List[Return]
