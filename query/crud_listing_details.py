from sqlalchemy.orm import Session
from datetime import date
from models import listing_details_models as models
from schemas import listing_details_schemas as schema
from schemas import category_schemas as schema_cat

#Booking
def create_booking(db: Session, 
                    booking: schema.BookingCreate,
                    guest_id: int,
                    listing_id: int):
    db_booking = models.Booking(**booking.dict(), guest_id=guest_id, listing_id=listing_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def get_booking(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def update_booking(db: Session, booking: schema.BookingUpdate, booking_data: schema.Booking):
    booking = booking.dict(exclude_unset=True)
    for key, value in booking.items():
        setattr(booking_data, key, value)
    db.commit()
    db.refresh(booking_data)
    return booking_data


def delete_booking(db: Session, booking: schema.Booking):
    if booking:
        db.delete(booking)
        db.commit()
        return {"ok": True}


#Review
def create_review(db: Session, guest_id: int,
                    listing_id: int, 
                    review: schema.ReviewCreate):
    db_review = models.Review(**review.dict(), 
                              listing_id=listing_id, 
                              guest_id=guest_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_review_by_id(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def update_review(db: Session, review: schema.ReviewUpdate, review_data: schema.Review):
    review = review.dict(exclude_unset=True)
    for attr, value in review.items():
        setattr(review_data, attr, value)  # update the attribute value
    db.add(review_data)
    db.commit()  # save changes to the database
    db.refresh(review_data)  # refresh the object to reflect the changes
    return review_data

def delete_review(db: Session, review: schema.Review):
    if review:
        db.delete(review)
        db.commit()
        return {"ok": True}


#Amenity
def create_amenity(db: Session,listing_id: int, amenity: schema.AmenityCreate):
    db_amenity = models.Amenity(**amenity.dict(), listing_id=listing_id)
    db.add(db_amenity)
    db.commit()
    db.refresh(db_amenity)
    return db_amenity

def get_amenity(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Amenity).offset(skip).limit(limit).all()

def get_amenity_by_id(db: Session, amenity_id: int):
    return db.query(models.Amenity).filter(models.Amenity.id == amenity_id).first()

def update_amenity(db: Session, amenity: schema.AmenityUpdate, amenity_data: schema.Amenity):
    amenity = amenity.dict(exclude_unset=True)
    for attr, value in amenity.items():
        setattr(amenity_data, attr, value)  # update the attribute value
    db.add(amenity_data)
    db.commit()  # save changes to the database
    db.refresh(amenity_data)  # refresh the object to reflect the changes
    return amenity_data

def delete_amenity(db: Session, amenity: schema.Amenity):
    if amenity:
        db.delete(amenity)
        db.commit()
        return {"ok": True}


#House Rules
def create_houserules(db: Session,listing_id: int, houserules: schema.HouseRulesCreate):
    db_houserules = models.HouseRules(**houserules.dict(), listing_id=listing_id)
    db.add(db_houserules)
    db.commit()
    db.refresh(db_houserules)
    return db_houserules


def get_houserules_by_id(db: Session, houserules_id: int):
    return db.query(models.HouseRules).filter(models.HouseRules.id == houserules_id).first()


def get_houserules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HouseRules).offset(skip).limit(limit).all()


def update_houserules(db: Session, houserules: schema.HouseRulesUpdate, houserules_data: schema.HouseRules):
    houserules = houserules.dict(exclude_unset=True)
    for attr, value in houserules.items():
        setattr(houserules_data, attr, value)  # update the attribute value
    db.add(houserules_data)
    db.commit()  # save changes to the database
    db.refresh(houserules_data)
    return houserules_data


def delete_houserules(db: Session, houserules: schema.HouseRules):
    if houserules:
        db.delete(houserules)
        db.commit()
        return {"ok": True}


#Favorite
def get_favorite_by_id(db: Session, favorite_id: int):
    return db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()


def get_favorites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Favorite).offset(skip).limit(limit).all()

def create_favorite(db: Session,  user_id:int, listing_id: int, favorite: schema.FavoriteCreate):
    db_favorite = models.Favorite(**favorite.dict(), user_id=user_id, listing_id=listing_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def update_favorite(db: Session, favorite: schema.FavoriteUpdate, favorite_date: models.Favorite):
    favorite = favorite.dict(exclude_unset=True)
    for key, value in favorite.items():
        setattr(favorite_date, key, value)
    db.commit()
    db.refresh(favorite_date)
    return favorite_date

def delete_favorite(db: Session, favorite: models.Favorite):
    if favorite:
        db.delete(favorite)
        db.commit()
        return {"ok": True}


#ListingCategory
def get_ListingCategory_by_id(db: Session, id: int):
    return db.query(models.ListingCategory).filter(models.ListingCategory.id == id).first()


def get_ListingCategory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ListingCategory).offset(skip).limit(limit).all()


def create_ListingCategory(db: Session, ListingCategory: schema_cat.ListingCategoryCreate):
    db_ListingCategory = models.ListingCategory(**ListingCategory.dict())
    db.add(db_ListingCategory)
    db.commit()
    db.refresh(db_ListingCategory)
    return db_ListingCategory

def update_ListingCategory(db: Session, listingcategory: schema_cat.ListingCategoryUpdate, listingcategory_data: schema_cat.ListingCategory):
    ListingCategory = listingcategory.dict(exclude_unset=True)
    for key, value in ListingCategory.items():
            setattr(listingcategory_data, key, value)
    db.add(listingcategory_data)
    db.commit()
    db.refresh(listingcategory_data)
    return listingcategory_data


def delete_ListingCategory(db: Session, listingcategory: schema_cat.ListingCategory):
    if listingcategory:
        db.delete(listingcategory)
        db.commit()
        return {"ok": True}



#Expiriences
def get_expiriences_by_id(db: Session, expiriences_id: int):
    return db.query(models.Expiriences).filter(models.Expiriences.id == expiriences_id).first()


def get_expiriences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Expiriences).offset(skip).limit(limit).all()

def create_expiriences(db: Session,  listing_id: int, expiriences: schema.ExpiriencesCreate):
    db_expiriences = models.Expiriences(**expiriences.dict(), listing_id=listing_id)
    db.add(db_expiriences)
    db.commit()
    db.refresh(db_expiriences)
    return db_expiriences

def update_expiriences(db: Session, expiriences: schema.ExpiriencesUpdate, expiriences_date: models.Expiriences):
    expiriences = expiriences.dict(exclude_unset=True)
    for key, value in expiriences.items():
        setattr(expiriences_date, key, value)
    db.commit()
    db.refresh(expiriences_date)
    return expiriences_date

def delete_expiriences(db: Session, expiriences: models.Expiriences):
    if expiriences:
        db.delete(expiriences)
        db.commit()
        return {"ok": True}


#ExpiriencesOrder
def get_ExpiriencesOrder_by_id(db: Session, user_id: int):
    return db.query(models.ExpiriencesOrder).filter(models.ExpiriencesOrder.id == user_id).first()


def get_ExpiriencesOrder(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExpiriencesOrder).offset(skip).limit(limit).all()


def create_ExpiriencesOrder(db: Session, guest_id: int,expiriences_id:int, ExpiriencesOrder: schema.ExpiriencesOrderCreate):
    db_ExpiriencesOrder = models.ExpiriencesOrder(**ExpiriencesOrder.dict(), guest_id=guest_id, expiriences_id=expiriences_id)
    db.add(db_ExpiriencesOrder)
    db.commit()
    db.refresh(db_ExpiriencesOrder)
    return db_ExpiriencesOrder

def update_ExpiriencesOrder(db: Session, user: schema.ExpiriencesOrderUpdate, user_data: schema.ExpiriencesOrder):
    ExpiriencesOrder_data = user.dict(exclude_unset=True)
    for key, value in ExpiriencesOrder_data.items():
            setattr(user_data, key, value)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def delete_ExpiriencesOrder(db: Session, user_id: schema.ExpiriencesOrder):
    if user_id:
        db.delete(user_id)
        db.commit()
        return {"ok": True}


#RestaurantMenu
def get_RestaurantMenu_by_id(db: Session, user_id: int):
    return db.query(models.RestaurantMenu).filter(models.RestaurantMenu.id == user_id).first()


def get_RestaurantMenu(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RestaurantMenu).offset(skip).limit(limit).all()


def create_RestaurantMenu(db: Session,listing_id:int, RestaurantMenu: schema.RestaurantMenuCreate):
    db_RestaurantMenu = models.RestaurantMenu(**RestaurantMenu.dict(), listing_id=listing_id)
    db.add(db_RestaurantMenu)
    db.commit()
    db.refresh(db_RestaurantMenu)
    return db_RestaurantMenu

def update_RestaurantMenu(db: Session, user: schema.RestaurantMenuUpdate, user_data: schema.RestaurantMenu):
    RestaurantMenu_data = user.dict(exclude_unset=True)
    for key, value in RestaurantMenu_data.items():
            setattr(user_data, key, value)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def delete_RestaurantMenu(db: Session, user_id: schema.RestaurantMenu):
    if user_id:
        db.delete(user_id)
        db.commit()
        return {"ok": True}


#RestaurantOrder
def get_RestauranteOrder_by_id(db: Session, user_id: int):
    return db.query(models.RestaurantOrder).filter(models.RestaurantOrder.id == user_id).first()


def get_RestauranteOrder(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RestaurantOrder).offset(skip).limit(limit).all()


def create_RestauranteOrder(db: Session, guest_id:int, restaurant_menu_id: int, RestaurantOrder: schema.RestaurantOrderCreate):
    db_RestaurantOrder = models.RestaurantOrder(**RestaurantOrder.dict(), guest_id=guest_id, restaurant_menu_id=restaurant_menu_id)
    db.add(db_RestaurantOrder)
    db.commit()
    db.refresh(db_RestaurantOrder)
    return db_RestaurantOrder

def update_RestauranteOrder(db: Session, user: schema.RestaurantOrderUpdate, user_data: schema.RestaurantOrder):
    RestaurantOrder_data = user.dict(exclude_unset=True)
    for key, value in RestaurantOrder_data.items():
            setattr(user_data, key, value)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def delete_RestauranteOrder(db: Session, user_id: schema.RestaurantOrder):
    if user_id:
        db.delete(user_id)
        db.commit()
        return {"ok": True}