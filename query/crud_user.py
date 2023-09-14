from sqlalchemy.orm import Session, joinedload
from datetime import date
from models import user_model as models
from schemas import user_schemas as schema

#find user_details by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).options(joinedload(models.User.user_data)).first()

#Get user_details
def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


#create appolice
def create_user(db: Session,
                   user: schema.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schema.UserUpdate, user_data: schema.User):
    user = user.dict(exclude_unset=True)
    for key, value in user.items():
            setattr(user_data, key, value)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def delete_user(db: Session, user: schema.User):
    if user:
        db.delete(user)
        db.commit()
        return {"ok": True}