from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text, DateTime, Boolean, Time, func
from sqlalchemy.orm import relationship
from database import Base

class UserDetails(Base):
    __tablename__ = 'user_details'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    Legal_name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    emergency_contacts = Column(String(255), nullable=False)
    government_id = Column(String(255), nullable=False)
    mpesa_contact_number = Column(String(20))
    mpesa_company_id = Column(String(20))

    user = relationship("User", back_populates='user_data')

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    creation_Date = Column(DateTime, default=func.now())


class UserRole(Base):
    __tablename__ = 'user_roles'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates='user_role')


class EmailConfirmation(Base):
    __tablename__ = 'email_confirmation'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    confirmation_code = Column(String(255), nullable=False)
    creation_Date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates='email_confirm')


class ProfilePicture(Base):
    __tablename__ = "profile_picture"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String)
    type = Column(String)
    creation_date = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates='profile_image')