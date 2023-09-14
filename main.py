from fastapi import FastAPI
from database import SessionLocal, engine, Base
from api import api_listing, api_listing_details, api_communication, api_user_details, api_user, api_payment

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(api_listing.router, prefix="/api")
app.include_router(api_listing_details.router, prefix="/api")
app.include_router(api_communication.router, prefix="/api")
app.include_router(api_payment.router, prefix="/api")
app.include_router(api_user.router, prefix="/api")
app.include_router(api_user_details.router, prefix="/api")