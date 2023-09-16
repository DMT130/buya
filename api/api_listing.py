from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from query import crud_listing as crud
from models import listing_model as models
from schemas import listing_schemas as schema
from database import SessionLocal, engine
from schemas import user_schemas as schema_user
from sqlalchemy.orm import Session
from typing import List 
from api.api_auth_user import get_current_active_user, check_admin_rights, get_current_user
#models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{host_id}/{category_id}/listing/", 
             response_model=schema.Listing, tags=["Listing"])
def create_listing(host_id:int, category_id:int, listing: schema.ListingCreate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_listing(db=db, listing=listing, 
                               host_id=host_id, 
                               category_id=category_id)


@router.get("/listing/", response_model=List[schema.Listing], tags=["Listing"])
def read_listing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_user)):
    db_listing = crud.get_listing(db, skip=skip, limit=limit)
    return db_listing

@router.get("/{listing_id}/listing/", response_model=schema.Listing, tags=["Listing"])
def read_listing(listing_id: int, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_user)):
    db_listing = crud.get_listing_by_id(db, listing_id)
    if not db_listing:
        raise HTTPException(status_code=404, detail="listing not found")
    return db_listing

@router.patch("/{listing_id}/listing/", response_model=schema.Listing, tags=["Listing"])
def update_listing(listing_id: int, listing_sch: schema.ListingUpdate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
     db_listing = crud.get_listing_by_id(db, listing_id)
     if not db_listing:
        raise HTTPException(status_code=404, detail="listing not found")
     result = crud.update_listing(db, listing_sch, db_listing)
     return result

@router.delete("/{listing_id}/listing/", tags=["Listing"])
def delete_listing(listing_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_listing = crud.get_listing_by_id(db, listing_id)
    if not db_listing:
        raise HTTPException(status_code=404, detail="listing not found")
    result = crud.delete_listing(db, db_listing)
    if result:
        raise HTTPException(status_code=200, detail="listing deleted")