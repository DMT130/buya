from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
#from schemas import user_details_schemas, listing_details_schemas


#Mensagem
class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    timestamp: date

    class Config:
        from_attributes = True


class MessageUpdate(MessageCreate):
    content: Optional[str] = None



#Mensagem
class NotificationBase(BaseModel):
    content: str
    read_status: bool


class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int
    timestamp: date

    class Config:
        from_attributes = True


class NotificationUpdate(NotificationCreate):
    content: Optional[str] = None
    read_status: Optional[bool] = None