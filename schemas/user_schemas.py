from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from schemas import user_details_schemas, listing_details_schemas


#User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserBaseCreate(UserBase):
    pass

class User(UserBase):
    id: int
    activated: bool
    Creation_Date: date
    Addition_user_data: list[user_details_schemas.UsedDetails] = []
    user_favorite_places: list[listing_details_schemas.Favorite] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBaseCreate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    activated: Optional[bool] = None