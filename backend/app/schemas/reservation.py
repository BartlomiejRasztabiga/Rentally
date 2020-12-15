from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.models.reservation import ReservationStatus


# Shared properties
class ReservationBase(BaseModel):
    car_id: int
    customer_id: int
    start_date: datetime
    end_date: datetime
    status: ReservationStatus


# Properties to receive via API on creation
class ReservationCreateDto(ReservationBase):
    pass


# Properties to receive via API on update
class ReservationUpdateDto(ReservationBase):
    pass


class ReservationInDBBase(ReservationBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Reservation(ReservationInDBBase):
    pass


# Additional properties stored in DB
class ReservationInDB(ReservationInDBBase):
    pass
