from fastapi import FastAPI
from database import engine, Base
from api import (api_listing, api_listing_details, 
                 api_communication, api_user_details, 
                 api_user, api_payment,
                   api_auth_user)

from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/ProfilePicture", StaticFiles(directory="ProfilePicture"), name="ProfilePicture")
app.mount("/ListingImages", StaticFiles(directory="ListingImages"), name="ListingImages")

app.include_router(api_auth_user.router, prefix="/api")
app.include_router(api_listing.router, prefix="/api")
app.include_router(api_listing_details.router, prefix="/api")
app.include_router(api_communication.router, prefix="/api")
app.include_router(api_payment.router, prefix="/api")
app.include_router(api_user.router, prefix="/api")
app.include_router(api_user_details.router, prefix="/api")