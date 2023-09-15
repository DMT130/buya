from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from schemas.user_details_schemas import UserDetails
from schemas import listing_details_schemas



#User
class UserBase(BaseModel):
    email: EmailStr
    

class User(UserBase):
    id: int
    activated: bool
    creation_Date: date
    Addition_user_data: list[UserDetails] = []
    user_favorite_places: list[listing_details_schemas.Favorite] = []

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    activated: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str