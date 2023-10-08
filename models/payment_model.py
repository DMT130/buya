from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship
from database import Base

class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bookings_id = Column(Integer, ForeignKey('bookings.id'))
    expiriences_list_id = Column(Integer, ForeignKey('expiriences_list.id'), nullable=True)
    restaurant_ticked_id = Column(Integer, ForeignKey('restaurant_ticked.id'), nullable=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=func.now())
    payment_method = Column(String(50), nullable=False)
    payment_direction = Column(String(50), nullable=False)
    payment_reference = Column(String(50), nullable=False)

    user = relationship("User", back_populates='user_payment')
    #order_restaurant = relationship("RestaurantOrder", back_populates='user_payment')
    user_booking = relationship("Booking", back_populates='user_payment')
    #order_expirience = relationship("ExpiriencesOrder", back_populates='user_payment')
    restaurant_backet = relationship("RestaurantTicked", back_populates='user_payment')
    expiriences_backet = relationship("ExpiriencesList", back_populates='user_payment')