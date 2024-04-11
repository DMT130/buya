from pydantic import BaseModel
from datetime import date
from typing import Optional


#UserDetails
class UserDetailsBase(BaseModel):
    Legal_name: str
    phone_number: str
    address: str
    emergency_contacts: str
    government_id: str
    mpesa_contact_number: Optional[str] = None
    mpesa_company_id: Optional[str] = None



class UserDetailsCreate(UserDetailsBase):
    pass

class UserDetails(UserDetailsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserDetailsUpdate(UserDetailsCreate):
    Legal_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contacts: Optional[str] = None
    government_id: Optional[str] = None
    mpesa_contact_number: Optional[str] = None
    mpesa_company_id: Optional[str] = None


#Role
class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    creation_Date: date

    class Config:
        from_attributes = True


class RoleUpdate(RoleCreate):
    name: Optional[str] = None


#UserRole
class UserRoleBase(BaseModel):
    pass


class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    id: int
    user_id: int
    role_id: int
    creation_Date: date

    class Config:
        from_attributes = True


class UserRoleUpdate(UserRoleCreate):
    role_id: Optional[int] = None



#Email Confirmation
class EmailConfirmationBase(BaseModel):
    confirmation_code: str


class EmailConfirmationCreate(EmailConfirmationBase):
    pass

class EmailConfirmation(EmailConfirmationBase):
    id: int
    user_id: int
    creation_Date: date

    class Config:
        from_attributes = True


class EmailConfirmationUpdate(EmailConfirmationCreate):
    confirmation_code: Optional[str] = None



#Profile Picture
class ProfilePictureBase(BaseModel):
    name: str
    path: str
    type: str
    


class ProfilePictureCreate(ProfilePictureBase):
    pass

class ProfilePicture(ProfilePictureBase):
    id: int
    user_id: int
    #creation_Date: date

    class Config:
        from_attributes = True


class ProfilePictureUpdate(ProfilePictureCreate):
    name: Optional[str] = None
    path: Optional[str] = None
    type: Optional[str] = None