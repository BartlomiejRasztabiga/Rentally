import enum

from sqlalchemy import Column, Enum, Float, Integer, Numeric, String

from app.db.base_class import Base


# fmt: off
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


# fmt: on


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
    price_per_day = Column(Numeric(10, 2), index=True, nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=True)
    mileage_limit = Column(Float, nullable=True)
    image_base64 = Column(String, nullable=True)

    # TRUCK RELATED
    loading_capacity = Column(Float, nullable=True, index=True)
    boot_width = Column(Float, nullable=True)
    boot_height = Column(Float, nullable=True)
    boot_length = Column(Float, nullable=True)

    # SPORTSCAR RELATED
    horsepower = Column(Integer, nullable=True, index=True)
    zero_to_hundred_time = Column(Float, nullable=True)
    engine_capacity = Column(Float, nullable=True)
