from pydantic import BaseModel
from typing import List
from Models.models import CustomizationType


class CustomizationPizza(BaseModel):
     pizza_option_id: int
     type:CustomizationType
     name:str
     price:float

class CustomizationPizzaCreate(CustomizationPizza):
    pass
class CustomizationPizzaUpdate(BaseModel):
    type: CustomizationType | None = None
    name: str | None = None
    price: float | None = None

class CustomizationPizzaResult(CustomizationPizza):
    id:int

    class Config:
        orm_mode=True
class CustomizationPizzaResponse(BaseModel):
    message:str
    data:CustomizationPizzaResult

class CustomizationPizzaListResponse(BaseModel):
    message:str
    data:List[CustomizationPizzaResult]