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
    picture_url: str



class UserDetailsCreate(UserDetailsBase):
    pass

class UserDetails(UserDetailsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserDetailsUpdate(UserDetailsCreate):
    Legal_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contacts: Optional[str] = None
    government_id: Optional[str] = None
    picture_url: Optional[str] = None



#Role
class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    creation_Date: date

    class Config:
        orm_mode = True


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
        orm_mode = True


class UserRoleUpdate(UserRoleCreate):
    role_id: Optional[int] = None