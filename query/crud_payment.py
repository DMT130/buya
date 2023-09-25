from sqlalchemy.orm import Session
from datetime import date
from models import payment_model as models
from schemas import payment_schemas as schema

#payment
def create_payment(db: Session, 
                    payment: schema.PaymentTransactionCreate,
                    user_id: int,
                    bookings_id: int,
                    expiriences_list_id: int=0,
                    restaurant_ticked_id: int=0
                    ):
    db_payment = models.PaymentTransaction(**payment.dict(), 
                        user_id=user_id, bookings_id=bookings_id,
                        expiriences_list_id=expiriences_list_id,
                        restaurant_ticked_id=restaurant_ticked_id)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment_by_id(db: Session, payment_id: int):
    return db.query(models.PaymentTransaction).filter(models.PaymentTransaction.id == payment_id).first()


def get_payment(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PaymentTransaction).offset(skip).limit(limit).all()


def update_payment(db: Session, payment: schema.PaymentTransactionUpdate, payment_data: schema.PaymentTransaction):
    payment = payment.dict(exclude_unset=True)
    for key, value in payment.items():
        setattr(payment_data, key, value)
    db.commit()
    db.refresh(payment_data)
    return payment_data


def delete_payment(db: Session, payment: schema.PaymentTransaction):
    if payment:
        db.delete(payment)
        db.commit()
        return {"ok": True}