import enum

from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base


class CarType(enum.Enum):
    CAR = "CAR"
    TRUCK = "TRUCK"
    SPORT = "SPORT"


class FuelType(enum.Enum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    HYBRID = "HYBRID"
    EV = "EV"


class GearboxType(enum.Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"


class AcType(enum.Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"


class DriveType(enum.Enum):
    FRONT = "FRONT"
    REAR = "REAR"
    ALL_WHEELS = "ALL_WHEELS"


class Car(Base):
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False)
    type = Column(Enum(CarType), index=True, nullable=False)
    fuel_type = Column(Enum(FuelType), index=True, nullable=False)
    gearbox_type = Column(Enum(GearboxType), index=True, nullable=False)
    ac_type = Column(Enum(AcType), index=True, nullable=False)
    number_of_passengers = Column(Integer, nullable=False)
    drive_type = Column(Enum(DriveType), index=True, nullable=False)
    average_consumption = Column(Float, nullable=True)
    number_of_airbags = Column(Integer, nullable=False)
    boot_capacity = Column(Float, nullable=True)
    price_per_day = Column(postgresql.MONEY, index=True, nullable=False)
    deposit_amount = Column(postgresql.MONEY, nullable=True)
    mileage_limit = Column(Float, nullable=True)
    image_base64 = Column(String, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "car", "polymorphic_on": type}
