import enum
from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base


class CarType(enum.Enum):
    CAR = 'CAR',
    TRUCK = 'TRUCK',
    SPORT = 'SPORT'


class FuelType(enum.Enum):
    PETROL = 'PETROL',
    DIESEL = 'DIESEL',
    HYBRID = 'HYBRID',
    EV = 'EV'


class GearboxType(enum.Enum):
    AUTO = 'AUTO',
    MANUAL = 'MANUAL'


class AcType(enum.Enum):
    AUTO = 'AUTO',
    MANUAL = 'MANUAL'


class DriveType(enum.Enum):
    FRONT = 'FRONT',
    REAR = 'REAR',
    ALL_WHEELS = 'ALL_WHEELS'


class Car(Base):
    id = Column(Integer, primary_key=True, index=True)
    modelName = Column(String, index=True, nullable=False)
    type = Column(Enum(CarType), nullable=False)
    fuelType = Column(Enum(FuelType), nullable=False)
    gearboxType = Column(Enum(GearboxType), nullable=False)
    acType = Column(Enum(AcType), nullable=False)
    numberOfPassengers = Column(Integer, nullable=False)
    driveType = Column(Enum(DriveType), nullable=False)
    averageConsumption = Column(Float, nullable=True)
    numberOfAirbags = Column(Integer, nullable=False)
    bootCapacity = Column(Float, nullable=True)
    pricePerDay = Column(postgresql.MONEY, nullable=False)
    depositAmount = Column(postgresql.MONEY, nullable=True)
    mileageLimit = Column(Float, nullable=True)
    imageBase64 = Column(String, nullable=True)
