from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from schemas import user_details_schemas as schema
import random
from query import crud_user as crud_urs
from query import crud_user_details as crud_det

class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME = "7a3e135c5807b0",
    MAIL_PASSWORD = "7a9dc71f1523ef",
    MAIL_FROM ="mailtrap@demomailtrap.com", #"admin@admin.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "sandbox.smtp.mailtrap.io",
    MAIL_FROM_NAME="buya",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def generate_confirmation_code(db:Session, user_id: int, low: int = 100000, high: int= 999999):
    random_int = str(random.randint(low, high))
    hash_random_int = str(hash(random_int))
    confirmation_obj = crud_det.create_confirmation_email(db, user_id, hash_random_int)
    saved_hashed_code = confirmation_obj.confirmation_code
    deleted_confirmation_code = crud_det.delete_confirmation_email(db, confirmation_obj)
    if deleted_confirmation_code is True:
        return saved_hashed_code, random_int
    else:
        raise HTTPException(status_code=404, detail="user not found")

def check_confirmation_code_match(db:Session, user_id: int, confirmation_code: int):
    confirmation_code = str(confirmation_code)
    hash_random_int = str(hash(confirmation_code))
    confirmation_code_hashed = crud_det.get_confirmation_email_by_user_id(db=db, user_id=user_id).confirmation_code
    if confirmation_code_hashed == hash_random_int:
        return True
    else:
        False


async def send_verification_email(email: EmailSchema, confirmation_code: int) -> JSONResponse:
    html = f"""<p>
               Hi this test mail, thanks for 
               using Fastapi-mail with second
               function just o see if it works
            </p> 
            <p>
               please use the code {confirmation_code} to activate your email
            </p> 
            """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return True