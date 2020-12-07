from typing import Optional

# Shared properties
from app.schemas.car import CarBase


class TruckBase(CarBase):
    loading_capacity: float
    boot_width: float
    boot_height: float
    boot_length: float


# Properties to receive via API on creation
class TruckCreateDto(TruckBase):
    pass


# Properties to receive via API on update
class TruckUpdateDto(TruckBase):
    pass


class TruckInDBBase(TruckBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Truck(TruckInDBBase):
    pass


# Additional properties stored in DB
class TruckInDB(TruckInDBBase):
    pass
