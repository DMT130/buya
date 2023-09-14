from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship

from database import Base

class ListingCategory(Base):
    __tablename__ = 'listing_category'
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)

    user_listing = relationship("Listing", back_populates='categories')



class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    total_number_of_bads = Column(Integer, nullable=False)
    total_number_of_people = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)
    creation_Date = Column(DateTime, default=func.now())
    

    user = relationship("User", back_populates='user_booking')
    user_listing = relationship("Listing", back_populates='user_booking')
    user_payment = relationship("PaymentTransaction", back_populates='user_booking')


class Expiriences(Base):
    __tablename__ = 'expiriences'

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    expirience_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_per_person = Column(Float, nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user_listing = relationship("Listing", back_populates='additional_services')
    order_expirience = relationship("ExpiriencesOrder", back_populates='additional_services')

class ExpiriencesOrder(Base):
    __tablename__ = 'expiriences_order'

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expiriences_id = Column(Integer, ForeignKey('expiriences.id'), nullable=False)
    date= Column(Date, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    total_cost  = Column(Float, nullable=False)

    user = relationship("User", back_populates='order_expirience')
    additional_services = relationship("Expiriences", back_populates='order_expirience')
    user_payment = relationship("PaymentTransaction", back_populates='order_expirience')


class RestaurantMenu(Base):
    __tablename__ = 'restaurant_menu'

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)

    user_listing = relationship("Listing", back_populates='menu_restaurant')
    order_restaurant = relationship("RestaurantOrder", back_populates='menu_restaurant')


class RestaurantOrder(Base):
    __tablename__ = 'restaurant_order'

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    restaurant_menu_id = Column(Integer, ForeignKey('restaurant_menu.id'), nullable=False)
    date = Column(Date, nullable=False)
    type_of_meal = Column(String)
    total_cost  = Column(Float, nullable=False) 

    user = relationship("User", back_populates='order_restaurant')
    menu_restaurant = relationship("RestaurantMenu", back_populates='order_restaurant')
    user_payment = relationship("PaymentTransaction", back_populates='order_restaurant')



class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    text_review = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    user = relationship("User", back_populates='user_review')
    user_listing = relationship("Listing", back_populates='user_review')

# Add more tables for amenities, images, favorites, messages, notifications, etc., as needed

class Amenity(Base):
    __tablename__ = 'amenities'
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    name = Column(String(50), nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user_listing = relationship("Listing", back_populates='listing_amenities')

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    image_url = Column(String(255), nullable=False)

    user_listing = relationship("Listing", back_populates='listing_image')

class HouseRules(Base):
    __tablename__ = 'house_rules'
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    rule_description = Column(String(255), nullable=False)
    checkin_after = Column(Time)
    checkout_before = Column(Time)
    allow_pets = Column(Boolean, default=False)
    allow_smoking = Column(Boolean, default=False)

    user_listing = relationship("Listing", back_populates='listing_rules')

# Add more fields as needed for house rules, such as additional details, rule categories, etc.


class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)

    user = relationship("User", back_populates='user_favorite')
    user_listing = relationship("Listing", back_populates='user_favorite')