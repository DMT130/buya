from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional
#from schemas import listing_schemas


#booking
class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    total_cost: float


class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    guest_id: int
    listing_id: int
    creation_Date: date
    #Addition_user_data: list[user_details_schemas.UsedDetails] = []

    class Config:
        orm_mode = True


class BookingUpdate(BookingCreate):
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    total_cost: Optional[float] = None


#Review
class ReviewBase(BaseModel):
    rating: int
    text_review: str


class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    guest_id: int
    listing_id: int
    timestamp: date
    #Addition_user_data: list[user_details_schemas.UsedDetails] = []

    class Config:
        orm_mode = True


class ReviewUpdate(ReviewCreate):
    rating: Optional[int] = None
    text_review: Optional[str] = None


#Amenity
class AmenityBase(BaseModel):
    name: str


class AmenityCreate(AmenityBase):
    pass

class Amenity(AmenityBase):
    id: int
    listing_id: int
    creation_Date: date
    #Addition_user_data: list[user_details_schemas.UsedDetails] = []

    class Config:
        orm_mode = True


class AmenityUpdate(AmenityCreate):
    name: Optional[str] = None


#Image
class ImageBase(BaseModel):
    image_url: str


class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    listing_id: int
    creation_Date: date
    #Addition_user_data: list[user_details_schemas.UsedDetails] = []

    class Config:
        orm_mode = True


class ImageUpdate(ImageCreate):
    image_url: Optional[str] = None


#HouseRules
class HouseRulesBase(BaseModel):
    rule_description: str
    checkin_after: time
    checkout_before: time
    allow_pets: bool
    allow_smoking: bool


class HouseRulesCreate(HouseRulesBase):
    pass

class HouseRules(HouseRulesBase):
    id: int
    listing_id: int
    #Addition_user_data: list[user_details_schemas.UsedDetails] = []

    class Config:
        orm_mode = True


class HouseRulesUpdate(HouseRulesCreate):
    rule_description: Optional[str] = None
    checkin_after: Optional[time] = None
    checkout_before: Optional[time] = None
    allow_pets: Optional[bool] = None
    allow_smoking: Optional[bool] = None


#Favorite
class FavoriteBase(BaseModel):
    pass

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    user_id: int
    listing_id: int
    
    class Config:
        orm_mode = True


class FavoriteUpdate(FavoriteCreate):
    pass


#Expiriences
class ExpiriencesBase(BaseModel):
    expirience_name: str
    description: str
    price: float


class ExpiriencesCreate(ExpiriencesBase):
    pass

class Expiriences(ExpiriencesBase):
    id: int
    listing_id: int

    class Config:
        orm_mode = True


class ExpiriencesUpdate(ExpiriencesCreate):
    expirience_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None