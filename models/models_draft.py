from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship
from database import Base


class UserDetails(Base):
    __tablename__ = 'user_details'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    Legal_name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    emergency_contacts = Column(String(255), nullable=False)
    government_id = Column(String(255), nullable=False)
    picture_url = Column(String(255), nullable=False)

    user = relationship("User", back_populates='user_data')

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    creation_Date = Column(DateTime, default=func.now())


class UserRole(Base):
    __tablename__ = 'user_roles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates='user_role')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
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

class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
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



class ListingCategory(Base):
    __tablename__ = 'listing_category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)

    user_listing = relationship("Listing", back_populates='categories')



class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
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

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    expirience_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_per_person = Column(Float, nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user_listing = relationship("Listing", back_populates='additional_services')
    order_expirience = relationship("ExpiriencesOrder", back_populates='additional_services')

class ExpiriencesOrder(Base):
    __tablename__ = 'expiriences_order'

    id = Column(Integer, primary_key=True)
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

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)

    user_listing = relationship("Listing", back_populates='menu_restaurant')
    order_restaurant = relationship("RestaurantOrder", back_populates='menu_restaurant')


class RestaurantOrder(Base):
    __tablename__ = 'restaurant_order'

    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    restaurant_menu_id = Column(Integer, ForeignKey('restaurant_menu.id'), nullable=False)
    date = Column(Date, nullable=False)
    type_of_meal = Column(String)
    total_cost  = Column(Float, nullable=False) 

    user = relationship("User", back_populates='order_restaurant')
    menu_restaurant = relationship("RestaurantMenu", back_populates='order_restaurant')
    user_payment = relationship("PaymentTransaction", back_populates='order_restaurant')

class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bookings_id = Column(Integer, ForeignKey('bookings.id'))
    expiriences_order_id = Column(Integer, ForeignKey('expiriences_order.id'))
    restaurant_order_id = Column(Integer, ForeignKey('restaurant_order.id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=func.now())
    payment_method = Column(String(50), nullable=False)

    user = relationship("User", back_populates='user_payment')
    order_restaurant = relationship("RestaurantOrder", back_populates='user_payment')
    user_booking = relationship("Booking", back_populates='user_payment')
    order_expirience = relationship("ExpiriencesOrder", back_populates='user_payment')

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
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
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    name = Column(String(50), nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user_listing = relationship("Listing", back_populates='listing_amenities')

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    image_url = Column(String(255), nullable=False)

    user_listing = relationship("Listing", back_populates='listing_image')

class HouseRules(Base):
    __tablename__ = 'house_rules'
    
    id = Column(Integer, primary_key=True)
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
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)

    user = relationship("User", back_populates='user_favorite')
    user_listing = relationship("Listing", back_populates='user_favorite')

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    read_status = Column(Boolean, default=False)

    user = relationship("User", back_populates='user_notification')

# Add more tables as needed for additional features such as geographical data and payment transactions

# Define roles and permissions as needed for your application
# For example:
# role = Role(name='admin')
# session.add(role)
# session.commit()