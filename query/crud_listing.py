from sqlalchemy.orm import Session
from datetime import date
from models import listing_model as models
from schemas import listing_schemas as schema

#find listing by ID
def get_listing_by_id(db: Session, listing_id: int):
    return db.query(models.Listing).filter(models.Listing.id == listing_id).first()

#Get listings
def get_listing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Listing).offset(skip).limit(limit).all()


#create appolice
def create_listing(db: Session,host_id:int,
                   category_id: int,  
                   listing: schema.ListingCreate):
    db_listing = models.Listing(**listing.dict(), 
                                host_id=host_id, 
                                category_id=category_id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

def update_listing(db: Session, listing: schema.ListingUpdate, listing_data: schema.Listing):
    listing = listing.dict(exclude_unset=True)
    for key, value in listing.items():
            setattr(listing_data, key, value)
    db.add(listing_data)
    db.commit()
    db.refresh(listing_data)
    return listing_data


def delete_listing(db: Session, listing: schema.Listing):
    if listing:
        db.delete(listing)
        db.commit()
        return {"ok": True}