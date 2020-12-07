from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class TruckBase(BaseModel):
    email: Optional[EmailStr] = None
    is_admin: bool = False
    full_name: Optional[str] = None


# # Properties to receive via API on creation
# class UserCreateDto(UserBase):
#     email: EmailStr
#     password: str
#
#
# # Properties to receive via API on update
# class UserUpdateDto(UserBase):
#     password: Optional[str] = None
#
#
# class UserInDBBase(UserBase):
#     id: Optional[int] = None
#
#     class Config:
#         orm_mode = True
#
#
# # Additional properties to return via API
# class User(UserInDBBase):
#     pass
#
#
# # Additional properties stored in DB
# class UserInDB(UserInDBBase):
#     hashed_password: str
