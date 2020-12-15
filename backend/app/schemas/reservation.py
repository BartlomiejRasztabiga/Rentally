from datetime import datetime
from typing import Optional

from app.models.reservation import ReservationStatus
from app.schemas.base import BaseModelWithOptionals


# Shared properties
class ReservationBase(BaseModelWithOptionals):
    car_id: int
    customer_id: int
    start_date: datetime
    end_date: datetime
    status: ReservationStatus


# Properties to receive via API on creation
class ReservationCreateDto(ReservationBase):
    pass


# Properties to receive via API on update
_update_optional_fields = ReservationBase.__fields__.keys()


# Properties to receive via API on update
class ReservationUpdateDto(ReservationBase, optional_fields=_update_optional_fields):
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
