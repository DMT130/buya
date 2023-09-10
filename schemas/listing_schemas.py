from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from schemas import listing_details_schemas


#Listing
class ListingBase(BaseModel):
    title: str
    description: str
    location: str
    price_per_night: float
    property_type: str
    number_of_badrooms: int
    number_of_bads: int
    number_of_bathrooms: int
    has_pool: bool
    has_free_parking: bool
    maximum_guests: int
    availability_calendar: str
    cancellation_policy: str
    safety_and_security_details: str
    latitude: float
    longitude: float


class ListingCreate(ListingBase):
    pass

class Listing(ListingBase):
    id: int
    host_id: int
    creation_Date: date
    Reviews: list[listing_details_schemas.Review] = []
    Amenities: list[listing_details_schemas.Amenity] = []
    Images: list[listing_details_schemas.Image] = []
    HouseRules: list[listing_details_schemas.HouseRules] = []

    class Config:
        orm_mode = True


class ListingUpdate(ListingCreate):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    price_per_night: Optional[float] = None
    property_type: Optional[str] = None
    number_of_badrooms: Optional[int] = None
    number_of_bads: Optional[int] = None
    number_of_bathrooms: Optional[int] = None
    has_pool: Optional[bool] = None
    has_free_parking: Optional[bool] = None
    maximum_guests: Optional[int] = None
    availability_calendar: Optional[str] = None
    cancellation_policy: Optional[str] = None
    safety_and_security_details: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None