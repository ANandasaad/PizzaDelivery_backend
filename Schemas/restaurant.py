from pydantic import BaseModel, Field
from typing import List
import  enum



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
    rating: float

    class Config:
        orm_mode = True

class RestaurantResponse(BaseModel):
    message: str
    data: Response

    class Config:
        from_attributes = True

class RestaurantListResponse(BaseModel):
    message: str
    total: int
    limit: int
    offset: int
    data: List[Response]
class UpdateRestaurant(Restaurant):
    rating:float
    class Config:
        orm_mode = True

class SortByRating(str, enum.Enum):
    ASC = "Low-to-High"  # Low to High
    DESC = "High-to-Low"  # High to Low

class FilterParams(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Number of records to fetch")
    offset: int = Field(0, ge=0, description="Number of records to skip")
    search: str = Field("", description="Search term for restaurants")
    sort: SortByRating | None = Field(None, description="Sort by Rating : High to Low or Low to High")

