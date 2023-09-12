from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
#from schemas import user_details_schemas, listing_details_schemas


#Mensagem
class PaymentTransactionBase(BaseModel):
    amount: float
    payment_method: str


class PaymentTransactionCreate(PaymentTransactionBase):
    pass

class PaymentTransaction(PaymentTransactionBase):
    id: int
    user_id: int
    bookings_id: Optional[int] = None
    expiriences_order_id: Optional[int] = None
    restaurant_order_id: Optional[int] = None
    payment_date: date

    class Config:
        orm_mode = True


class PaymentTransactionUpdate(PaymentTransactionCreate):
    amount: Optional[float] = None
    payment_method: Optional[str] = None