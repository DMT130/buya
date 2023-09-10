from fastapi import Depends, APIRouter, HTTPException
from query import crud_comunication as crud
from models import models
from schemas import comunication_schemas as schema
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List 


models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}/notification/", 
                response_model=schema.Notification, tags=["Notification"])
def create_notification(user_id:int, notification: schema.NotificationCreate, 
                        db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification, 
                               user_id=user_id)


@router.get("/notification/", response_model=List[schema.Notification], tags=["Notification"])
def read_notification(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_notification = crud.get_notification(db, skip=skip, limit=limit)
    return db_notification

@router.get("/{notification_id}/notification/", response_model=schema.Notification, tags=["Notification"])
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification_by_id(db, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="notification not found")
    return db_notification

@router.patch("/{notification_id}/notification/", response_model=schema.Notification, tags=["Notification"])
def update_notification(notification_id: int, notification_sch: schema.NotificationUpdate, db: Session = Depends(get_db)):
     db_notification = crud.get_notification_by_id(db, notification_id)
     if not db_notification:
        raise HTTPException(status_code=404, detail="notification not found")
     result = crud.update_notification(db, notification_sch, db_notification)
     return result

@router.delete("/{notification_id}/notification/", tags=["Notification"])
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification_by_id(db, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="notification not found")
    result = crud.delete_notification(db, db_notification)
    if result:
        raise HTTPException(status_code=200, detail="notification deleted")


#Message
@router.post("/{sender_id}/{receiver_id}/message/", 
               response_model=schema.Message, tags=["Message"])
def create_message(sender_id:int, receiver_id:int, 
                   message: schema.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message, 
                               sender_id=sender_id, 
                               receiver_id=receiver_id)


@router.get("/message/", response_model=List[schema.Message], tags=["Message"])
def read_message(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, skip=skip, limit=limit)
    return db_message

@router.get("/{message_id}/message/", response_model=schema.Message, tags=["Message"])
def read_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message_by_id(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="message not found")
    return db_message

@router.patch("/{message_id}/message/", response_model=schema.Message, tags=["Message"])
def update_message(message_id: int, message_sch: schema.MessageUpdate, db: Session = Depends(get_db)):
     db_message = crud.get_message_by_id(db, message_id)
     if not db_message:
        raise HTTPException(status_code=404, detail="message not found")
     result = crud.update_message(db, message_sch, db_message)
     return result

@router.delete("/{message_id}/message/", tags=["Message"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message_by_id(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="message not found")
    result = crud.delete_message(db, db_message)
    if result:
        raise HTTPException(status_code=200, detail="message deleted")