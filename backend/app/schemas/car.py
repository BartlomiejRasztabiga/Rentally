from typing import Optional

from pydantic import BaseModel

# Shared properties
from app.models.car import CarType, FuelType, GearboxType, AcType, DriveType


class CarBase(BaseModel):
    model_name: str
    type: CarType
    fuel_type: FuelType
    gearbox_type: GearboxType
    ac_type: AcType
    number_of_passengers: int
    drive_type: DriveType
    average_consumption: Optional[float]
    number_of_airbags: int
    boot_capacity: Optional[float]
    price_per_day: str
    deposit_amount: Optional[str]
    mileage_limit: Optional[float]
    image_base64: Optional[str]


# Properties to receive via API on creation
class CarCreateDto(CarBase):
    pass


# Properties to receive via API on update
class CarUpdateDto(CarBase):
    pass


class CarInDBBase(CarBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Car(CarInDBBase):
    pass


# Additional properties stored in DB
class CarInDB(CarInDBBase):
    pass