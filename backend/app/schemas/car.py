from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

# Shared properties
from app.models.car import AcType, CarType, DriveType, FuelType, GearboxType


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
    price_per_day: Decimal
    deposit_amount: Optional[Decimal]
    mileage_limit: Optional[float]
    image_base64: Optional[str]

    # TRUCK RELATED
    loading_capacity: Optional[float]
    boot_width: Optional[float]
    boot_height: Optional[float]
    boot_length: Optional[float]

    # SPORTSCAR RELATED
    horsepower: Optional[int]
    zero_to_hundred_time: Optional[float]
    engine_capacity: Optional[float]

    def __init_subclass__(cls, optional_fields=None, **kwargs):
        """
        allow some fields of subclass turn into optional
        """
        super().__init_subclass__(**kwargs)
        if optional_fields:
            for field in optional_fields:
                cls.__fields__[field].outer_type_ = Optional
                cls.__fields__[field].required = False


# Properties to receive via API on creation
class CarCreateDto(CarBase):
    pass


# Properties to receive via API on update
_update_optional_fields = CarBase.__fields__.keys()


class CarUpdateDto(CarBase, optional_fields=_update_optional_fields):
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
