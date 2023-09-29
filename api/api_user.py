from fastapi import Depends, APIRouter, HTTPException
from query import crud_user as crud
from schemas import user_schemas as schema
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List 
from query.crud_email_verification import send_verification_email, generate_confirmation_code, check_confirmation_code_match
from api.api_auth_user import get_current_active_user, get_current_user, check_admin_rights


#models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/user/", response_model=schema.User, tags=["User"])
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    created_used = crud.create_user(db=db, user=user)
    _, random_int = await generate_confirmation_code(db=db, user_id=created_used.id)
    sent = await send_verification_email(email=user.email, confirmation_code=random_int)
    if sent is True:
        return created_used
        


@router.get("/user/", response_model=List[schema.User], tags=["User"])
def read_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schema.User=Depends(check_admin_rights)):
    db_user = crud.get_user(db, skip=skip, limit=limit)
    return db_user


@router.get("/{user_id}/user/", response_model=schema.User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schema.User=Depends(get_current_user)):
    if current_user.id != user_id:
         raise HTTPException(status_code=403, detail="You can only read your own user")
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@router.patch("/{user_id}/user/", response_model=schema.User, tags=["User"])
def update_user(user_id: int, user_sch: schema.UserUpdate, db: Session = Depends(get_db), current_user: schema.User=Depends(get_current_user)):
     if current_user.id != user_id:
         raise HTTPException(status_code=403, detail="You can only update your own user")
     db_user = crud.get_user_by_id(db, user_id)
     if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
     result = crud.update_user(db, user_sch, db_user)
     return result

@router.patch("/{user_id}/{confirmation_code}/user/", response_model=schema.User, tags=["User"])
def activate_user(user_id: int, confirmation_code: int, user_sch: schema.UserActivation, 
                  db: Session = Depends(get_db), 
                  current_user: schema.User=Depends(get_current_user)):
     if current_user.id != user_id:
         raise HTTPException(status_code=403, detail="You can only activate your own user")
     db_user = crud.get_user_by_id(db, user_id)
     if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
     confirmation = check_confirmation_code_match(db, user_id=user_id, confirmation_code=confirmation_code)
     if confirmation is True:
        result = crud.update_user(db, user_sch, db_user)
     else:
         raise HTTPException(status_code=403, detail="The confirmation code does not match")
     return result


@router.delete("/{user_id}/user/", tags=["User"])
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schema.User=Depends(get_current_user)):
    if current_user.id != user_id:
         raise HTTPException(status_code=403, detail="You can only delete your own user")
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    result = crud.delete_user(db, db_user)
    if result:
        raise HTTPException(status_code=200, detail="user deleted")
