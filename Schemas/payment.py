from pydantic import BaseModel
from typing import Optional, List


class PaymentBase(BaseModel):
    order_id: int
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str



class PaymentCreate(PaymentBase):
    pass

class PaymentEntity(BaseModel):
    id: str
    entity: str
    amount: int
    currency: str
    status: str
    order_id: str
    invoice_id: Optional[str]
    international: bool
    method: str
    amount_refunded: int
    refund_status: Optional[str]
    captured: bool
    description: Optional[str]
    card_id: Optional[str]
    bank: Optional[str]
    wallet: Optional[str]
    vpa: Optional[str]
    email: Optional[str]
    contact: Optional[str]
    notes: dict
    fee: int
    tax: int
    error_code: Optional[str]
    error_description: Optional[str]
    error_source: Optional[str]
    error_step: Optional[str]
    error_reason: Optional[str]
    acquirer_data: Optional[dict]
    created_at: int
    reward: Optional[str]

class OrderEntity(BaseModel):
    id: str
    entity: str
    amount: int
    amount_paid: int
    amount_due: int
    currency: str
    receipt: Optional[str]
    offer_id: Optional[str]
    status: str
    attempts: int
    notes: List[str]
    created_at: int

class Payload(BaseModel):
    payment: Optional[PaymentEntity]
    order: Optional[OrderEntity]

class WebhookEvent(BaseModel):
    event: str
    payload: Payload
class WebhookResponse(BaseModel):
    message: str
    data: WebhookEvent