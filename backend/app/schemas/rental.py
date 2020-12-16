from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.models.rental import RentalStatus
from app.schemas import Car, Customer, Reservation


# Shared properties
class RentalBase(BaseModel):
    car_id: int
    customer_id: int
    reservation_id: Optional[int]
    start_date: datetime
    end_date: datetime
    status: RentalStatus


# Properties to receive via API on creation
class RentalCreateDto(RentalBase):
    pass


# Properties to receive via API on update
class RentalUpdateDto(RentalBase):
    pass


class RentalInDBBase(RentalBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Rental(RentalInDBBase):
    car: Optional[Car] = None
    customer: Optional[Customer] = None
    reservation: Optional[Reservation] = None


# Additional properties stored in DB
class RentalInDB(RentalInDBBase):
    pass
