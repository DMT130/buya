from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from query import crud_payment as crud
from models import payment_model as models
from schemas import payment_schemas as schema
from query import crud_listing_details as crud_sh
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List 
from api.api_auth_user import get_current_active_user, check_admin_rights, get_current_user
from schemas import user_schemas as schema_user

#models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}/{bookings_id}/payment/", 
             response_model=schema.PaymentTransaction, tags=["Payment Transaction"])
def create_payment(user_id:int, bookings_id:int,
                    payment: schema.PaymentTransactionCreate, 
                   db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user),
                   expiriences_list_id:int=0,
                   restaurant_ticked_id: int=0):

    booking = crud_sh.get_booking_by_id(db, bookings_id).total_cost
    expiriece_amount =0
    restaurant_amount =0

    try:

        expirience = crud_sh.get_All_ExpiriencesOrder_by_id(db, expiriences_list_id)
        for i in expirience:
            expiriece_amount+=i.total_cost

    except:
        expirience=0
    
    try:
        order_user = crud_sh.get_All_RestauranteOrder_by_ticked_id(db, restaurant_ticked_id)
        for i in order_user:
            restaurant_amount+=i.total_cost
    except:
        order_user=0

    
    payment.amount = booking+expiriece_amount+restaurant_amount

    if expiriences_list_id == 0:
        expiriences_list_id = None
    if restaurant_ticked_id == 0:
        restaurant_ticked_id = None

    return crud.create_payment(db=db, payment=payment, user_id=user_id, 
                               bookings_id=bookings_id, restaurant_ticked_id=restaurant_ticked_id,
                               expiriences_list_id=expiriences_list_id)


@router.get("/payment/", response_model=List[schema.PaymentTransaction], tags=["Payment Transaction"])
def read_payment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_active_user)):
    db_payment = crud.get_payment(db, skip=skip, limit=limit)
    return db_payment

@router.get("/{payment_id}/payment/", response_model=schema.PaymentTransaction, tags=["Payment Transaction"])
def read_payment(payment_id: int, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(get_current_active_user)):
    db_payment = crud.get_payment_by_id(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")
    return db_payment

@router.patch("/{payment_id}/payment/", response_model=schema.PaymentTransaction, tags=["Payment Transaction"])
def update_payment(payment_id: int, payment_sch: schema.PaymentTransactionUpdate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
     db_payment = crud.get_payment_by_id(db, payment_id)
     if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")
     result = crud.update_payment(db, payment_sch, db_payment)
     return result

@router.delete("/{payment_id}/payment/", tags=["Payment Transaction"])
def delete_payment(payment_id: int, db: Session = Depends(get_db), 
                   current_user: schema_user.User=Depends(get_current_active_user)):
    db_payment = crud.get_payment_by_id(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")
    result = crud.delete_payment(db, db_payment)
    if result:
        raise HTTPException(status_code=200, detail="payment deleted")