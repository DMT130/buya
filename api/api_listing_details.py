from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from query import crud_listing_details as crud
from query import crud_listing as crud_list
from models import listing_details_models as models
from schemas import listing_details_schemas as schema
from schemas import category_schemas as schemas_cat
from database import SessionLocal, engine
from schemas import user_schemas as schema_user
from sqlalchemy.orm import Session
from typing import List 
from api.api_auth_user import get_current_active_user, get_current_user
import shutil, os

#models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Booking
@router.post("/{listing_id}/{guest_id}/booking/", 
             response_model=schema.Booking, tags=["booking"])
def create_booking(listing_id:int, guest_id:int, 
                   booking: schema.BookingCreate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
    listing = crud_list.get_listing_by_id(db, listing_id)
    date_delta = booking.check_out_date - booking.check_in_date
    booking.total_cost = date_delta.days*listing.price_per_night*booking.number_of_rooms
    return crud.create_booking(db=db, booking=booking, 
                               guest_id=guest_id, 
                               listing_id=listing_id)


@router.get("/booking/", response_model=List[schema.Booking], tags=["booking"])
def read_booking(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_active_user)):
    db_booking = crud.get_booking(db, skip=skip, limit=limit)
    return db_booking

@router.get("/{booking_id}/booking/", response_model=schema.Booking, tags=["booking"])
def read_booking(booking_id: int, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_active_user)):
    db_booking = crud.get_booking_by_id(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="booking not found")
    return db_booking

@router.patch("/{booking_id}/booking/", response_model=schema.Booking, tags=["booking"])
def update_booking(booking_id: int, booking_sch: schema.BookingUpdate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
     db_booking = crud.get_booking_by_id(db, booking_id)
     if not db_booking:
        raise HTTPException(status_code=404, detail="booking not found")
     result = crud.update_booking(db, booking_sch, db_booking)
     return result

@router.delete("/{booking_id}/booking/", tags=["booking"])
def delete_booking(booking_id: int, db: Session = Depends(get_db), 
                   current_user: schema_user.User=Depends(get_current_active_user)):
    db_booking = crud.get_booking_by_id(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="booking not found")
    result = crud.delete_booking(db, db_booking)
    if result:
        raise HTTPException(status_code=200, detail="booking deleted")


#Review
@router.post("/{listing_id}/{guest_id}/review/", 
response_model=schema.Review, tags=["Review"])
def create_review(listing_id:int, guest_id:int, review: schema.ReviewCreate, 
    db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_review(db=db, review=review, 
                               listing_id=listing_id, 
                               guest_id=guest_id)


@router.get("/review/", response_model=List[schema.Review], tags=["Review"])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_user)):
    db_review = crud.get_reviews(db, skip=skip, limit=limit)
    return db_review

@router.get("/{review_id}/review/", response_model=schema.Review, tags=["Review"])
def read_review(review_id: int, db: Session = Depends(get_db),
                current_user: schema_user.User=Depends(get_current_user)):
    db_review = crud.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="review not found")
    return db_review

@router.patch("/{review_id}/review/", response_model=schema.Review, tags=["Review"])
def update_review(review_id: int, review_sch: schema.ReviewUpdate, db: Session = Depends(get_db),
                  current_user: schema_user.User=Depends(get_current_active_user)):
     db_review = crud.get_review_by_id(db, review_id)
     if not db_review:
        raise HTTPException(status_code=404, detail="review not found")
     result = crud.update_review(db, review_sch, db_review)
     return result

@router.delete("/{review_id}/review/", tags=["Review"])
def delete_review(review_id: int, db: Session = Depends(get_db),
                  current_user: schema_user.User=Depends(get_current_active_user)):
    db_review = crud.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="review not found")
    result = crud.delete_review(db, db_review)
    if result:
        raise HTTPException(status_code=200, detail="review deleted")


#Amenity
@router.post("/{listing_id}/amenity/", response_model=schema.Amenity, tags=["Amenity"])
def create_amenity(listing_id:int,  amenity: schema.AmenityCreate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_amenity(db=db, amenity=amenity, listing_id=listing_id)


@router.get("/amenity/", response_model=List[schema.Amenity], tags=["Amenity"])
def read_amenitys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  current_user: schema_user.User=Depends(get_current_user)):
    db_amenity = crud.get_amenity(db, skip=skip, limit=limit)
    return db_amenity

@router.get("/{amenity_id}/amenity/", response_model=schema.Amenity, tags=["Amenity"])
def read_amenity(amenity_id: int, db: Session = Depends(get_db), 
                 current_user: schema_user.User=Depends(get_current_user)):
    db_amenity = crud.get_amenity_by_id(db, amenity_id)
    if not db_amenity:
        raise HTTPException(status_code=404, detail="amenity not found")
    return db_amenity

@router.patch("/{amenity_id}/amenity/", response_model=schema.Amenity, tags=["Amenity"])
def update_amenity(amenity_id: int, amenity_sch: schema.AmenityUpdate, db: Session = Depends(get_db), 
                   current_user: schema_user.User=Depends(get_current_active_user)):
     db_amenity = crud.get_amenity_by_id(db, amenity_id)
     if not db_amenity:
        raise HTTPException(status_code=404, detail="amenity not found")
     result = crud.update_amenity(db, amenity_sch, db_amenity)
     return result

@router.delete("/{amenity_id}/amenity/", tags=["Amenity"])
def delete_amenity(amenity_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_amenity = crud.get_amenity_by_id(db, amenity_id)
    if not db_amenity:
        raise HTTPException(status_code=404, detail="amenity not found")
    result = crud.delete_amenity(db, db_amenity)
    if result:
        raise HTTPException(status_code=200, detail="amenity deleted")


#House Rules
@router.post("/{listing_id}/houserules/", response_model=schema.HouseRules, tags=["House Rules"])
def create_houserules(listing_id:int,  houserules: schema.HouseRulesCreate, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_houserules(db=db, houserules=houserules, listing_id=listing_id)


@router.get("/houserules/", response_model=List[schema.HouseRules], tags=["House Rules"])
def read_houserules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                    current_user: schema_user.User=Depends(get_current_user)):
    db_houserules = crud.get_houserules(db, skip=skip, limit=limit)
    return db_houserules

@router.get("/{houserules_id}/houserules/", response_model=schema.HouseRules, tags=["House Rules"])
def read_houserules_by_id(houserules_id: int, db: Session = Depends(get_db), 
                          current_user: schema_user.User=Depends(get_current_user)):
    db_houserules = crud.get_houserules_by_id(db, houserules_id)
    if not db_houserules:
        raise HTTPException(status_code=404, detail="houserules not found")
    return db_houserules

@router.patch("/{houserules_id}/houserules/", response_model=schema.HouseRules, tags=["House Rules"])
def update_houserules(houserules_id: int, houserules_sch: schema.HouseRulesUpdate, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
     db_houserules = crud.get_houserules_by_id(db, houserules_id)
     if not db_houserules:
        raise HTTPException(status_code=404, detail="houserules not found")
     result = crud.update_houserules(db, houserules_sch, db_houserules)
     return result

@router.delete("/{houserules_id}/houserules/", tags=["House Rules"])
def delete_houserules(houserules_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_houserules = crud.get_houserules_by_id(db, houserules_id)
    if not db_houserules:
        raise HTTPException(status_code=404, detail="houserules not found")
    result = crud.delete_houserules(db, db_houserules)
    if result:
        raise HTTPException(status_code=200, detail="houserules deleted")


#Favorite
@router.post("/{user_id}/{listing_id}/favorite/",
              response_model=schema.Favorite, tags=["Favorite"])
def create_favorite(user_id:int, listing_id:int,
                    favorite: schema.FavoriteCreate, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_favorite(db=db, favorite=favorite, 
                               user_id=user_id, listing_id=listing_id)


@router.get("/favorite/", response_model=List[schema.Favorite], tags=["Favorite"])
def read_favorite(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_favorite = crud.get_favorites(db, skip=skip, limit=limit)
    return db_favorite

@router.get("/{favorite_id}/favorite/", response_model=schema.Favorite, tags=["Favorite"])
def read_favorite(favorite_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_favorite = crud.get_favorite_by_id(db, favorite_id)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="favorite not found")
    return db_favorite

@router.patch("/{favorite_id}/favorite/", response_model=schema.Favorite, tags=["Favorite"])
def update_favorite(favorite_id: int, favorite_sch: schema.FavoriteUpdate, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
     db_favorite = crud.get_favorite_by_id(db, favorite_id)
     if not db_favorite:
        raise HTTPException(status_code=404, detail="favorite not found")
     result = crud.update_favorite(db, favorite_sch, db_favorite)
     return result

@router.delete("/{favorite_id}/favorite/", tags=["Favorite"])
def delete_favorite(favorite_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_favorite = crud.get_favorite_by_id(db, favorite_id)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="favorite not found")
    result = crud.delete_favorite(db, db_favorite)
    if result:
        raise HTTPException(status_code=200, detail="favorite deleted")


#ListingCategory
@router.post("/ListingCategory/", response_model=schemas_cat.ListingCategory, tags=["Listing Category"])
def create_ListingCategory(ListingCategory: schemas_cat.ListingCategoryCreate, db: Session = Depends(get_db), 
                           current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_ListingCategory(db=db, ListingCategory=ListingCategory)


@router.get("/ListingCategory/", response_model=List[schemas_cat.ListingCategory], tags=["Listing Category"])
def read_ListingCategory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                         current_user: schema_user.User=Depends(get_current_user)):
    db_ListingCategory = crud.get_ListingCategory(db, skip=skip, limit=limit)
    return db_ListingCategory

@router.get("/{ListingCategory_id}/ListingCategory/", response_model=schemas_cat.ListingCategory, tags=["Listing Category"])
def read_ListingCategory(ListingCategory_id: int, db: Session = Depends(get_db), 
                         current_user: schema_user.User=Depends(get_current_user)):
    db_ListingCategory = crud.get_ListingCategory_by_id(db, ListingCategory_id)
    if not db_ListingCategory:
        raise HTTPException(status_code=404, detail="ListingCategory not found")
    return db_ListingCategory

@router.patch("/{ListingCategory_id}/ListingCategory/", response_model=schemas_cat.ListingCategory, tags=["Listing Category"])
def update_ListingCategory(ListingCategory_id: int, ListingCategory_sch: schemas_cat.ListingCategoryUpdate, db: Session = Depends(get_db), 
                           current_user: schema_user.User=Depends(get_current_active_user)):
     db_ListingCategory = crud.get_ListingCategory_by_id(db, ListingCategory_id)
     if not db_ListingCategory:
        raise HTTPException(status_code=404, detail="ListingCategory not found")
     result = crud.update_ListingCategory(db, ListingCategory_sch, db_ListingCategory)
     return result

@router.delete("/{ListingCategory_id}/ListingCategory/", tags=["Listing Category"])
def delete_ListingCategory(ListingCategory_id: int, db: Session = Depends(get_db), 
                           current_user: schema_user.User=Depends(get_current_active_user)):
    db_ListingCategory = crud.get_ListingCategory_by_id(db, ListingCategory_id)
    if not db_ListingCategory:
        raise HTTPException(status_code=404, detail="ListingCategory not found")
    result = crud.delete_ListingCategory(db, db_ListingCategory)
    if result:
        raise HTTPException(status_code=200, detail="ListingCategory deleted")


#Expiriences
@router.post("/{listing_id}/expiriences/", response_model=schema.Expiriences, tags=["Expiriences"])
def create_expiriences(listing_id:int, expiriences: schema.ExpiriencesCreate, db: Session = Depends(get_db), 
                       current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_expiriences(db=db, expiriences=expiriences, 
                               listing_id=listing_id)


@router.get("/expiriences/", response_model=List[schema.Expiriences], tags=["Expiriences"])
def read_expiriences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                     current_user: schema_user.User=Depends(get_current_user)):
    db_expiriences = crud.get_expiriences(db, skip=skip, limit=limit)
    return db_expiriences

@router.get("/{expiriences_id}/expiriences/", response_model=schema.Expiriences, tags=["Expiriences"])
def read_expiriences(expiriences_id: int, db: Session = Depends(get_db), 
                     current_user: schema_user.User=Depends(get_current_user)):
    db_expiriences = crud.get_expiriences_by_id(db, expiriences_id)
    if not db_expiriences:
        raise HTTPException(status_code=404, detail="expiriences not found")
    return db_expiriences

@router.patch("/{expiriences_id}/expiriences/", response_model=schema.Expiriences, tags=["Expiriences"])
def update_expiriences(expiriences_id: int, expiriences_sch: schema.ExpiriencesUpdate, db: Session = Depends(get_db), 
                       current_user: schema_user.User=Depends(get_current_active_user)):
     db_expiriences = crud.get_expiriences_by_id(db, expiriences_id)
     if not db_expiriences:
        raise HTTPException(status_code=404, detail="expiriences not found")
     result = crud.update_expiriences(db, expiriences_sch, db_expiriences)
     return result

@router.delete("/{expiriences_id}/expiriences/", tags=["Expiriences"])
def delete_expiriences(expiriences_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_expiriences = crud.get_expiriences_by_id(db, expiriences_id)
    if not db_expiriences:
        raise HTTPException(status_code=404, detail="expiriences not found")
    result = crud.delete_expiriences(db, db_expiriences)
    if result:
        raise HTTPException(status_code=200, detail="expiriences deleted")


#ExpiriencesList
@router.post("/{user_id}/ExpiriencesList/", response_model=schema.ExpiriencesList, tags=["Expiriences List"])
def create_ExpiriencesList(user_id:int, ExpiriencesList: schema.ExpiriencesListCreate, db: Session = Depends(get_db),
                           current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_ExpiriencesList(db=db, ExpiriencesList=ExpiriencesList, user_id=user_id)


@router.get("/ExpiriencesList/", response_model=List[schema.ExpiriencesList], tags=["Expiriences List"])
def read_ExpiriencesList(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                         current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesList = crud.get_ExpiriencesList(db, skip=skip, limit=limit)
    return db_ExpiriencesList

@router.get("/{ExpiriencesList_id}/ExpiriencesList/", response_model=schema.ExpiriencesList, tags=["Expiriences List"])
def read_ExpiriencesList(ExpiriencesList_id: int, db: Session = Depends(get_db),
                         current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesList = crud.get_ExpiriencesList_by_id(db, ExpiriencesList_id)
    if not db_ExpiriencesList:
        raise HTTPException(status_code=404, detail="ExpiriencesList not found")
    return db_ExpiriencesList

@router.patch("/{ExpiriencesList_id}/ExpiriencesList/", response_model=schema.ExpiriencesList, tags=["Expiriences List"])
def update_ExpiriencesList(ExpiriencesList_id: int, ExpiriencesList_sch: schema.ExpiriencesListUpdate, db: Session = Depends(get_db),
                           current_user: schema_user.User=Depends(get_current_active_user)):
     db_ExpiriencesList = crud.get_ExpiriencesList_by_id(db, ExpiriencesList_id)
     if not db_ExpiriencesList:
        raise HTTPException(status_code=404, detail="ExpiriencesList not found")
     result = crud.update_ExpiriencesList(db, ExpiriencesList_sch, db_ExpiriencesList)
     return result

@router.delete("/{ExpiriencesList_id}/ExpiriencesList/", tags=["Expiriences List"])
def delete_ExpiriencesList(ExpiriencesList_id: int, db: Session = Depends(get_db),
                           current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesList = crud.get_ExpiriencesList_by_id(db, ExpiriencesList_id)
    if not db_ExpiriencesList:
        raise HTTPException(status_code=404, detail="ExpiriencesList not found")
    result = crud.delete_ExpiriencesList(db, db_ExpiriencesList)
    if result:
        raise HTTPException(status_code=200, detail="ExpiriencesList deleted")


#ExpiriencesOrder
@router.post("/{guest_id}/{expiriences_id}/{expiriences_list_id}/expiriences_order/",
               response_model=schema.ExpiriencesOrder, tags=["Expiriences Order"])
def create_ExpiriencesOrder(guest_id:int, expiriences_id:int, expiriences_list_id:int,
           ExpiriencesOrder: schema.ExpiriencesOrderCreate, db: Session = Depends(get_db), 
           current_user: schema_user.User=Depends(get_current_active_user)):
    #total _cost = price_person*number_of_people*number_of_repetition
    db_expiriences = crud.get_expiriences_by_id(db, expiriences_id)
    ExpiriencesOrder.total_cost = db_expiriences.price_per_person*ExpiriencesOrder.number_of_people*ExpiriencesOrder.number_of_repetition
    return crud.create_ExpiriencesOrder(db=db, ExpiriencesOrder=ExpiriencesOrder, 
                               guest_id=guest_id, 
                               expiriences_id=expiriences_id,
                               expiriences_list_id=expiriences_list_id)


@router.get("/ExpiriencesOrder/", response_model=List[schema.ExpiriencesOrder], tags=["Expiriences Order"])
def read_ExpiriencesOrder(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesOrder = crud.get_ExpiriencesOrder(db, skip=skip, limit=limit)
    return db_ExpiriencesOrder

@router.get("/{ExpiriencesOrder_id}/ExpiriencesOrder/", response_model=schema.ExpiriencesOrder, tags=["Expiriences Order"])
def read_ExpiriencesOrder(ExpiriencesOrder_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesOrder = crud.get_ExpiriencesOrder_by_id(db, ExpiriencesOrder_id)
    if not db_ExpiriencesOrder:
        raise HTTPException(status_code=404, detail="ExpiriencesOrder not found")
    return db_ExpiriencesOrder

@router.patch("/{ExpiriencesOrder_id}/ExpiriencesOrder/", response_model=schema.ExpiriencesOrder, tags=["Expiriences Order"])
def update_ExpiriencesOrder(ExpiriencesOrder_id: int, ExpiriencesOrder_sch: schema.ExpiriencesOrderUpdate, db: Session = Depends(get_db),
                            current_user: schema_user.User=Depends(get_current_active_user)):
     db_ExpiriencesOrder = crud.get_ExpiriencesOrder_by_id(db, ExpiriencesOrder_id)
     if not db_ExpiriencesOrder:
        raise HTTPException(status_code=404, detail="ExpiriencesOrder not found")
     result = crud.update_ExpiriencesOrder(db, ExpiriencesOrder_sch, db_ExpiriencesOrder)
     return result

@router.delete("/{ExpiriencesOrder_id}/ExpiriencesOrder/", tags=["Expiriences Order"])
def delete_ExpiriencesOrder(ExpiriencesOrder_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_ExpiriencesOrder = crud.get_ExpiriencesOrder_by_id(db, ExpiriencesOrder_id)
    if not db_ExpiriencesOrder:
        raise HTTPException(status_code=404, detail="ExpiriencesOrder not found")
    result = crud.delete_ExpiriencesOrder(db, db_ExpiriencesOrder)
    if result:
        raise HTTPException(status_code=200, detail="ExpiriencesOrder deleted")



#RestaurantMenu
@router.post("/{listing_id}/RestaurantMenu/", 
              response_model=schema.RestaurantMenu, tags=["Restaurant Menu"])
def create_RestaurantMenu(listing_id:int, RestaurantMenu: schema.RestaurantMenuCreate, 
                        db: Session = Depends(get_db), 
                        current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_RestaurantMenu(db=db, RestaurantMenu=RestaurantMenu, listing_id=listing_id)


@router.get("/RestaurantMenu/", response_model=List[schema.RestaurantMenu], tags=["Restaurant Menu"])
def read_RestaurantMenu(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                        current_user: schema_user.User=Depends(get_current_user)):
    db_RestaurantMenu = crud.get_RestaurantMenu(db, skip=skip, limit=limit)
    return db_RestaurantMenu

@router.get("/{RestaurantMenu_id}/RestaurantMenu/", response_model=schema.RestaurantMenu, tags=["Restaurant Menu"])
def read_RestaurantMenu(RestaurantMenu_id: int, db: Session = Depends(get_db), 
                        current_user: schema_user.User=Depends(get_current_user)):
    db_RestaurantMenu = crud.get_RestaurantMenu_by_id(db, RestaurantMenu_id)
    if not db_RestaurantMenu:
        raise HTTPException(status_code=404, detail="RestaurantMenu not found")
    return db_RestaurantMenu

@router.patch("/{RestaurantMenu_id}/RestaurantMenu/", response_model=schema.RestaurantMenu, tags=["Restaurant Menu"])
def update_RestaurantMenu(RestaurantMenu_id: int, RestaurantMenu_sch: schema.RestaurantMenuUpdate, db: Session = Depends(get_db),
                          current_user: schema_user.User=Depends(get_current_active_user)):
     db_RestaurantMenu = crud.get_RestaurantMenu_by_id(db, RestaurantMenu_id)
     if not db_RestaurantMenu:
        raise HTTPException(status_code=404, detail="RestaurantMenu not found")
     result = crud.update_RestaurantMenu(db, RestaurantMenu_sch, db_RestaurantMenu)
     return result

@router.delete("/{RestaurantMenu_id}/RestaurantMenu/", tags=["Restaurant Menu"])
def delete_RestaurantMenu(RestaurantMenu_id: int, db: Session = Depends(get_db),
                          current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestaurantMenu = crud.get_RestaurantMenu_by_id(db, RestaurantMenu_id)
    if not db_RestaurantMenu:
        raise HTTPException(status_code=404, detail="RestaurantMenu not found")
    result = crud.delete_RestaurantMenu(db, db_RestaurantMenu)
    if result:
        raise HTTPException(status_code=200, detail="RestaurantMenu deleted")


#RestaurantTicked API
@router.post("/{user_id}/RestaurantTicked/", response_model=schema.RestaurantTicked, tags=["Restaurant Ticked"])
def create_RestaurantTicked(user_id:int, RestaurantTicked: schema.RestaurantTickedCreate, db: Session = Depends(get_db),
                            current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_RestaurantTicked(db=db, RestaurantTicked=RestaurantTicked, user_id=user_id)


@router.get("/RestaurantTicked/", response_model=List[schema.RestaurantTicked], tags=["Restaurant Ticked"])
def read_RestaurantTicked(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                          current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestaurantTicked = crud.get_RestaurantTicked(db, skip=skip, limit=limit)
    return db_RestaurantTicked

@router.get("/{RestaurantTicked_id}/RestaurantTicked/", response_model=schema.RestaurantTicked, tags=["Restaurant Ticked"])
def read_RestaurantTicked(RestaurantTicked_id: int, db: Session = Depends(get_db),
                          current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestaurantTicked = crud.get_RestaurantTicked_by_id(db, RestaurantTicked_id)
    if not db_RestaurantTicked:
        raise HTTPException(status_code=404, detail="RestaurantTicked not found")
    return db_RestaurantTicked

@router.patch("/{RestaurantTicked_id}/RestaurantTicked/", response_model=schema.RestaurantTicked, tags=["Restaurant Ticked"])
def update_RestaurantTicked(RestaurantTicked_id: int, RestaurantTicked_sch: schema.RestaurantTickedUpdate, db: Session = Depends(get_db),
                            current_user: schema_user.User=Depends(get_current_active_user)):
     db_RestaurantTicked = crud.get_RestaurantTicked_by_id(db, RestaurantTicked_id)
     if not db_RestaurantTicked:
        raise HTTPException(status_code=404, detail="RestaurantTicked not found")
     result = crud.update_RestaurantTicked(db, RestaurantTicked_sch, db_RestaurantTicked)
     return result

@router.delete("/{RestaurantTicked_id}/RestaurantTicked/", tags=["Restaurant Ticked"])
def delete_RestaurantTicked(RestaurantTicked_id: int, db: Session = Depends(get_db),
                            current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestaurantTicked = crud.get_RestaurantTicked_by_id(db, RestaurantTicked_id)
    if not db_RestaurantTicked:
        raise HTTPException(status_code=404, detail="RestaurantTicked not found")
    result = crud.delete_RestaurantTicked(db, db_RestaurantTicked)
    if result:
        raise HTTPException(status_code=200, detail="RestaurantTicked deleted")


#RestauranteOrder
@router.post("/{guest_id}/{restaurant_menu_id}/{restaurant_ticked_id}/RestauranteOrder/", 
              response_model=schema.RestaurantOrder, tags=["Restaurante Order"])
def create_RestauranteOrder(guest_id:int, restaurant_menu_id:int, restaurant_ticked_id:int,
                            RestauranteOrder: schema.RestaurantOrderCreate, 
                            db: Session = Depends(get_db), 
                            current_user: schema_user.User=Depends(get_current_active_user)):
    restaurant_menu = crud.get_RestaurantMenu_by_id(db, restaurant_menu_id)
    RestauranteOrder.total_cost = RestauranteOrder.number_of_meals*restaurant_menu.price
    return crud.create_RestauranteOrder(db=db, RestaurantOrder=RestauranteOrder, 
                               guest_id=guest_id, 
                               restaurant_menu_id=restaurant_menu_id,
                               restaurant_ticked_id=restaurant_ticked_id)


@router.get("/RestauranteOrder/", response_model=List[schema.RestaurantOrder], tags=["Restaurante Order"])
def read_RestauranteOrder(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                          current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestauranteOrder = crud.get_RestauranteOrder(db, skip=skip, limit=limit)
    return db_RestauranteOrder

@router.get("/{RestauranteOrder_id}/RestauranteOrder/", response_model=schema.RestaurantOrder, tags=["Restaurante Order"])
def read_RestauranteOrder(RestauranteOrder_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestauranteOrder = crud.get_RestauranteOrder_by_id(db, RestauranteOrder_id)
    if not db_RestauranteOrder:
        raise HTTPException(status_code=404, detail="RestauranteOrder not found")
    return db_RestauranteOrder

@router.patch("/{RestauranteOrder_id}/RestauranteOrder/", response_model=schema.RestaurantOrder, tags=["Restaurante Order"])
def update_RestauranteOrder(RestauranteOrder_id: int, RestauranteOrder_sch: schema.RestaurantOrderUpdate, db: Session = Depends(get_db),
                            current_user: schema_user.User=Depends(get_current_active_user)):
     db_RestauranteOrder = crud.get_RestauranteOrder_by_id(db, RestauranteOrder_id)
     if not db_RestauranteOrder:
        raise HTTPException(status_code=404, detail="RestauranteOrder not found")
     result = crud.update_RestauranteOrder(db, RestauranteOrder_sch, db_RestauranteOrder)
     return result

@router.delete("/{RestauranteOrder_id}/RestauranteOrder/", tags=["Restaurante Order"])
def delete_RestauranteOrder(RestauranteOrder_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_RestauranteOrder = crud.get_RestauranteOrder_by_id(db, RestauranteOrder_id)
    if not db_RestauranteOrder:
        raise HTTPException(status_code=404, detail="RestauranteOrder not found")
    result = crud.delete_RestauranteOrder(db, db_RestauranteOrder)
    if result:
        raise HTTPException(status_code=200, detail="RestauranteOrder deleted")
    

#Listing Images
@router.post("/listing-images/", tags=["Listing Images"])
def create_upload_files(listing_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    for file in files:
        filename = file.filename
        file_path = os.path.join("ListingImages", filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        image = models.Image(listing_id=listing_id, image_url=file_path)
        db.add(image)
        db.commit()
        db.refresh(image)
    return {"filenames": [file.filename for file in files]}

#update Images
@router.put("/listing-images/{image_id}", tags=["Listing Images"])
def update_image(image_id: int, image: schema.ImageUpdate, db: Session = Depends(get_db)):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    for field, value in image.dict(exclude_unset=True).items():
        setattr(db_image, field, value)
    db.commit()
    db.refresh(db_image)
    return db_image

#delete Images
@router.delete("/listing-images/{image_id}", tags=["Listing Images"])
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    shutil.rmtree(db_image.image_url, ignore_errors=False, onerror=None)
    db.delete(db_image)
    db.commit()
    return {"message": "Image deleted successfully"}

#Real all Images
@router.get("/listing-images/", response_model=List[schema.Image], tags=["Listing Images"])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = db.query(models.Image).offset(skip).limit(limit).all()
    return images

#Real one Images
@router.get("/listing-images/{image_id}", response_model=schema.Image, tags=["Listing Images"])
def read_one_image(image_id: int, db: Session = Depends(get_db)):
    images = db.query(models.Image).filter(models.Image.id == image_id).first()
    return images

#Real one listing
@router.get("/listing-images/{listing_id}", response_model=List[schema.Image], tags=["Listing Images"])
def read_image_by_listing(listing_id: int, db: Session = Depends(get_db)):
    images = db.query(models.Image).filter(models.Image.listing_id == listing_id).all()
    return images