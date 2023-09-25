from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional
#from schemas import listing_schemas


#booking
class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    total_number_of_bads: int
    total_number_of_people: int
    number_of_rooms: int
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
    total_number_of_bads: Optional[int] = None
    total_number_of_people: Optional[int] = None
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
    price_per_person: float


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
    price_per_person: Optional[float] = None



#ExpiriencesOrder
class ExpiriencesOrderBase(BaseModel):
    number_of_people: int
    number_of_repetition: int
    total_cost: float


class ExpiriencesOrderCreate(ExpiriencesOrderBase):
    pass

class ExpiriencesOrder(ExpiriencesOrderBase):
    id: int
    guest_id: int
    expiriences_id: int
    expiriences_list_id: int

    class Config:
        orm_mode = True


class ExpiriencesOrderUpdate(ExpiriencesOrderCreate):
    number_of_people: Optional[int] = None
    total_cost: Optional[float] = None
    number_of_repetition:  Optional[int] = None


#Restaurante
class RestaurantMenuBase(BaseModel):
    name: str
    description: str
    price: float
    category: str


class RestaurantMenuCreate(RestaurantMenuBase):
    pass

class RestaurantMenu(RestaurantMenuBase):
    id: int
    listing_id: int

    class Config:
        orm_mode = True


class RestaurantMenuUpdate(RestaurantMenuCreate):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


#RestauranteOrder
class RestaurantOrderBase(BaseModel):
    date: date
    type_of_meal: str
    total_cost: float
    number_of_meals: int


class RestaurantOrderCreate(RestaurantOrderBase):
    pass

class RestaurantOrder(RestaurantOrderBase):
    id: int
    guest_id: int
    restaurant_menu_id: int
    restaurant_ticked_id: int

    class Config:
        orm_mode = True


class RestaurantOrderUpdate(RestaurantOrderCreate):
    date: Optional[date] = None
    type_of_meal: Optional[str] = None
    total_cost: Optional[float] = None
    number_of_meals: Optional[int] = None



#RestaurantTicked
class RestaurantTickedBase(BaseModel):
    pass


class RestaurantTickedCreate(RestaurantTickedBase):
    pass

class RestaurantTicked(RestaurantTickedBase):
    id: int
    user_id: int
    creating_date: date

    class Config:
        orm_mode = True


class RestaurantTickedUpdate(RestaurantTickedCreate):
    user_id: Optional[int] = None



#ExpiriencesList
class ExpiriencesListBase(BaseModel):
    pass


class ExpiriencesListCreate(ExpiriencesListBase):
    pass

class ExpiriencesList(ExpiriencesListBase):
    id: int
    user_id: int
    creating_date: date

    class Config:
        orm_mode = True


class ExpiriencesListUpdate(ExpiriencesListCreate):
    user_id: Optional[int] = None