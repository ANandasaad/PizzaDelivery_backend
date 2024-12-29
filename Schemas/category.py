from pydantic import BaseModel
from typing import List


class Category(BaseModel):
    name: str

class CategoryCreate(Category):
    pass

class CategoryUpdate(Category):
    pass


class Response(Category):
    id: int

    class Config:
        orm_mode = True
class CategoryResponse(BaseModel):
    message: str
    data: Response

class CategoryListResponse(BaseModel):
    message: str
    data:List[Response]