from pydantic import BaseModel

from Models.models import OrderStatus, PaymentStatus
from typing import List




class Order(BaseModel):
    customer_id: int
    quantity: int
    address: str
    total_price: float
    status:OrderStatus
    payment_status:PaymentStatus

class CustomizationOption(BaseModel):
    customization_id: int

class OrderItem(BaseModel):
    pizza_option_id: int
    quantity: int
    customizations:List[CustomizationOption] | None=None

    class Config:
        schema_extra = {
            "example": {
                "pizza_option_id": 3,
                "quantity": 2,
                "customizations": [
                    {"customization_option_id": 1},
                    {"customization_option_id": 2}
                ]
            }
        }




class OrderCreate(Order):
      items:List[OrderItem]

      class Config:
        schema_extra = {
            "example": {
                "customer_id": 1,
                "quantity": 2,
                "address": "123 Main St",
                "total_price": 100.0,
                "status": "pending",
                "payment_status": "pending",
                "items": [
                    {
                        "pizza_option_id": 1,
                        "quantity": 2,
                        "customizations": [
                            {"customization_option_id": 1},
                            {"customization_option_id": 2}
                        ]
                    }
                ]
            }
        }

