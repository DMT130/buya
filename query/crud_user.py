from sqlalchemy.orm import Session
from models import user_model as models
from schemas import user_schemas as schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


#find user_details by ID
def get_user_by_id(db: Session, user_id: int):
    try: 
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return user
    except:
        return False

def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    except:
        return False

#Get user_details
def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


#create appolice
def create_user(db: Session, user: schema.UserCreate):
    new_pass = get_password_hash(user.password)
    user.password = new_pass
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