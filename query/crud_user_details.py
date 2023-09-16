from sqlalchemy.orm import Session
from datetime import date
from models import user_details_models as models
from schemas import user_details_schemas as schema

#find user_details by ID
def get_user_details_by_id(db: Session, user_details_id: int):
    return db.query(models.UserDetails).filter(models.UserDetails.id == user_details_id).first()

#Get user_details
def get_user_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserDetails).offset(skip).limit(limit).all()


#create appolice
def create_user_details(db: Session,
                   user_id: int,  
                   user_details: schema.UserDetailsCreate):
    db_user_details = models.UserDetails(**user_details.dict(), 
                                user_id=user_id)
    db.add(db_user_details)
    db.commit()
    db.refresh(db_user_details)
    return db_user_details

def update_user_details(db: Session, 
                        user_details: schema.UserDetailsUpdate, 
                        user_details_data: schema.UserDetails):
    user_details = user_details.dict(exclude_unset=True)
    for key, value in user_details.items():
            setattr(user_details_data, key, value)
    db.add(user_details_data)
    db.commit()
    db.refresh(user_details_data)
    return user_details_data


def delete_user_details(db: Session, user_details: schema.UserDetails):
    if user_details:
        db.delete(user_details)
        db.commit()
        return {"ok": True}



#Role
def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

#Get user_details
def get_role(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


#create appolice
def create_role(db: Session, role: schema.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role: schema.RoleUpdate, role_data: schema.Role):
    role = role.dict(exclude_unset=True)
    for key, value in role.items():
            setattr(role_data, key, value)
    db.add(role_data)
    db.commit()
    db.refresh(role_data)
    return role_data


def delete_role(db: Session, role: schema.Role):
    if role:
        db.delete(role)
        db.commit()
        return {"ok": True}



#UserRole
def get_userole_by_id(db: Session, userole_id: int):
    return db.query(models.UserRole).filter(models.UserRole.id == userole_id).first()

def get_userole_by_user_id(db: Session, user_id: int):
    return db.query(models.UserRole).filter(models.UserRole.user_id == user_id).first()

#Get user_details
def get_userole(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserRole).offset(skip).limit(limit).all()


#create userole
def create_userole(db: Session,user_id:int, role_id: int, userole: schema.UserRoleCreate):
    db_userole = models.UserRole(**userole.dict(), user_id=user_id, role_id=role_id)
    db.add(db_userole)
    db.commit()
    db.refresh(db_userole)
    return db_userole

def update_userole(db: Session, userole: schema.UserRoleUpdate, userole_data: schema.UserRole):
    userole = userole.dict(exclude_unset=True)
    for key, value in userole.items():
            setattr(userole_data, key, value)
    db.add(userole_data)
    db.commit()
    db.refresh(userole_data)
    return userole_data


def delete_userole(db: Session, userole: schema.UserRole):
    if userole:
        db.delete(userole)
        db.commit()
        return {"ok": True}