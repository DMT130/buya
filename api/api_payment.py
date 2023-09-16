from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from query import crud_payment as crud
from models import payment_model as models
from schemas import payment_schemas as schema
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


@router.post("/{user_id}/{bookings_id}/{expiriences_order_id}/{restaurant_order_id}/payment/", 
              response_model=schema.PaymentTransaction, tags=["Payment Transaction"])
def create_payment(user_id:int, bookings_id:int,expiriences_order_id:int, 
                   restaurant_order_id: int, payment: schema.PaymentTransactionCreate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(get_current_active_user)):
    return crud.create_payment(db=db, payment=payment, 
                               Customer_ID=user_id, 
                               bookings_id=bookings_id, 
                               expiriences_order_id=expiriences_order_id,
                               restaurant_order_id=restaurant_order_id)


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
def delete_payment(payment_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(get_current_active_user)):
    db_payment = crud.get_payment_by_id(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")
    result = crud.delete_payment(db, db_payment)
    if result:
        raise HTTPException(status_code=200, detail="payment deleted")