from typing import Optional

from pydantic.main import BaseModel


# Shared properties
class CustomerBase(BaseModel):
    full_name: str
    address: Optional[str]
    phone_number: Optional[str]


# Properties to receive via API on creation
class CustomerCreateDto(CustomerBase):
    pass


# Properties to receive via API on update
class CustomerUpdateDto(CustomerBase):
    pass


class CustomerInDBBase(CustomerBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Customer(CustomerInDBBase):
    pass


# Additional properties stored in DB
class CustomerInDB(CustomerInDBBase):
    pass
