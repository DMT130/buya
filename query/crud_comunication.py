from sqlalchemy.orm import Session
from datetime import date
from models import communication_model as models
from schemas import comunication_schemas as schema

#Booking
def create_notification(db: Session, 
                    notification: schema.NotificationCreate,
                    user_id: int):
    db_notification = models.Notification(**notification.dict(), user_id=user_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notification_by_id(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()


def get_notification(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).offset(skip).limit(limit).all()


def update_notification(db: Session, notification: schema.NotificationUpdate, notification_data: schema.Notification):
    notification = notification.dict(exclude_unset=True)
    for key, value in notification.items():
        setattr(notification_data, key, value)
    db.commit()
    db.refresh(notification_data)
    return notification_data


def delete_notification(db: Session, notification: schema.Notification):
    if notification:
        db.delete(notification)
        db.commit()
        return {"ok": True}



#Mensagem
def create_message(db: Session, 
                    message: schema.MessageCreate,
                    sender_id: int,
                    receiver_id: int):
    db_messagem = models.Message(**message.dict(), sender_id=sender_id, receiver_id=receiver_id)
    db.add(db_messagem)
    db.commit()
    db.refresh(db_messagem)
    return db_messagem


def get_message_by_id(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()


def get_message(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def update_message(db: Session, message: schema.MessageUpdate, message_data: schema.Message):
    messagem = message.dict(exclude_unset=True)
    for key, value in messagem.items():
        setattr(message_data, key, value)
    db.commit()
    db.refresh(message_data)
    return message_data


def delete_message(db: Session, message: schema.Message):
    if message:
        db.delete(message)
        db.commit()
        return {"ok": True}