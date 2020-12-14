from typing import Optional

from app.schemas.base import BaseModelWithOptionals


# Shared properties
class CustomerBase(BaseModelWithOptionals):
    full_name: str
    address: Optional[str]
    phone_number: Optional[str]


# Properties to receive via API on creation
class CustomerCreateDto(CustomerBase):
    pass


# Properties to receive via API on update
_update_optional_fields = CustomerBase.__fields__.keys()


# Properties to receive via API on update
class CustomerUpdateDto(CustomerBase, optional_fields=_update_optional_fields):
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
