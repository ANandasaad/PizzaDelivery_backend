
import enum

from pydantic import BaseModel, Field

from Models.models import PizzaType
from typing import List

from Schemas.customization import CustomizationPizzaResult


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
    customizations: List[CustomizationPizzaResult]
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
    total: int
    limit: int
    offset: int
    data: List[PizzaResult]

class SortOrder(str, enum.Enum):
    ASC = "Low-to-High"  # Low to High
    DESC = "High-to-Low"   # High to Low
class FilterParams(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Number of records to fetch")
    offset: int = Field(0, ge=0, description="Number of records to skip")
    search: str = Field("", description="Search term for pizza options")
    type: PizzaType | None = Field(None, description="List of pizza types to filter by")
    sort: SortOrder | None = Field(None, description="Sort by price : High to Low or Low to High")

