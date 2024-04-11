from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional, List
from schemas import listing_schemas


#Category
class ListingCategoryBase(BaseModel):
    category_name: str


class ListingCategoryCreate(ListingCategoryBase):
    pass

class ListingCategory(ListingCategoryBase):
    id: int
    listings: List[listing_schemas.Listing] = []

    class Config:
        from_attributes = True


class ListingCategoryUpdate(ListingCategoryCreate):
    category_name: Optional[str] = None
