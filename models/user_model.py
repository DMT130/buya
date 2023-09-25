from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship

from database import Base



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    creation_Date = Column(DateTime, default=func.now())
    activated = Column(Boolean, default=False)
    # Add more user profile fields as needed

    user_data = relationship("UserDetails", back_populates='user')
    user_role = relationship("UserRole", back_populates='user')
    user_listing = relationship("Listing", back_populates='user')
    user_booking = relationship("Booking", back_populates='user')
    user_review = relationship("Review", back_populates='user')
    user_favorite = relationship("Favorite", back_populates='user')
    user_notification = relationship("Notification", back_populates='user')
    user_payment = relationship("PaymentTransaction", back_populates='user')
    order_expirience = relationship("ExpiriencesOrder", back_populates='user')
    order_restaurant = relationship("RestaurantOrder", back_populates='user')
    restaurant_backet = relationship("RestaurantTicked", back_populates='user')
    expiriences_backet = relationship("ExpiriencesList", back_populates='user')