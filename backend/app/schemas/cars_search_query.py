import abc
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql.elements import BinaryExpression

from app.models import Car
from app.models.car import AcType, CarType, DriveType, FuelType, GearboxType


class RangeCriterion(BaseModel):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_condition(self) -> BinaryExpression:
        raise NotImplementedError()


class NumberOfPassengersRange(RangeCriterion):
    start: int
    end: int

    def to_condition(self) -> BinaryExpression:
        return Car.number_of_passengers.between(self.start, self.end)


class PricePerDayRange(RangeCriterion):
    start: float
    end: float

    def to_condition(self) -> BinaryExpression:
        return Car.price_per_day.between(self.start, self.end)


class AvailabilityDatesRange(BaseModel):
    start: datetime
    end: datetime


class CarsSearchQuery(BaseModel):
    model_name: Optional[str] = None
    type: Optional[CarType] = None
    fuel_type: Optional[FuelType] = None
    gearbox_type: Optional[GearboxType] = None
    ac_type: Optional[AcType] = None
    drive_type: Optional[DriveType] = None
    number_of_passengers: Optional[NumberOfPassengersRange] = None
    price_per_day: Optional[PricePerDayRange] = None
    availability_dates: Optional[AvailabilityDatesRange] = None

    def to_conditions(self) -> List[BinaryExpression]:
        """
        Returns list of SQLAlchemy filter conditions based on query object values
        """
        conditions = []
        for field_name in CarsSearchQuery.__fields__.keys():
            value = getattr(self, field_name)
            if value is not None:
                if isinstance(value, RangeCriterion):
                    conditions.append(value.to_condition())
                elif isinstance(
                    value, str
                ):  # use ilike on str fields instead of exact match
                    conditions.append(getattr(Car, field_name).ilike(f"%{value}%"))
                elif isinstance(value, AvailabilityDatesRange):  # skip
                    pass
                else:
                    conditions.append(getattr(Car, field_name) == value)
        return conditions
