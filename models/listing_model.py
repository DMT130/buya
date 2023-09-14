from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship

from database import Base


class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('listing_category.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    price_per_night = Column(Float, nullable=False)
    property_type = Column(String(50))
    number_of_badrooms = Column(Integer, nullable=False)
    number_of_bads = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    numbrt_of_livingroms = Column(Integer, nullable=False)
    numbrt_of_diningroms = Column(Integer, nullable=False)
    number_of_avaliable_badrooms = Column(Integer, nullable=False)
    has_pool = Column(Boolean, default=False)
    has_free_parking = Column(Boolean, default=False)
    has_free_breakfast = Column(Boolean, default=False)
    has_free_restaurant = Column(Boolean, default=False)
    maximum_guests = Column(Integer, nullable=False)
    availability_calendar = Column(Text)
    cancellation_policy = Column(String(50), nullable=True)
    safety_and_security_details = Column(Text)
    creation_Date = Column(DateTime, default=func.now())
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # Add more listing details as needed 

    user = relationship("User", back_populates='user_listing')
    user_booking = relationship("Booking", back_populates='user_listing')
    user_review = relationship("Review", back_populates='user_listing')
    user_favorite = relationship("Favorite", back_populates='user_listing')
    listing_amenities = relationship("Amenity", back_populates='user_listing')
    listing_rules = relationship("HouseRules", back_populates='user_listing')
    categories = relationship("ListingCategory", back_populates='user_listing')
    listing_image = relationship("Image", back_populates='user_listing')
    additional_services = relationship("Expiriences", back_populates='user_listing')
    menu_restaurant = relationship("RestaurantMenu", back_populates='user_listing')