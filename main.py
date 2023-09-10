from fastapi import FastAPI
from models import models
from database import SessionLocal, engine
from api import api_listing, api_listing_details, api_communication, api_user_details

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.include_router(api_listing.router, tags=["Listing"], prefix="/api")
app.include_router(api_listing_details.router, prefix="/api")
app.include_router(api_communication.router, prefix="/api")
app.include_router(api_user_details.router, prefix="/api")