from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship
from database import Base

class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
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