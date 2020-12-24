from decimal import Decimal

from sqlalchemy.orm import Session

from app import models, services
from app.models.car import AcType, CarType, DriveType, FuelType, GearboxType
from app.schemas.car import CarCreateDto


def get_test_car_create_dto() -> CarCreateDto:
    car_create_dto = CarCreateDto(
        model_name="test",
        type=CarType.CAR,
        fuel_type=FuelType.DIESEL,
        gearbox_type=GearboxType.AUTO,
        ac_type=AcType.AUTO,
        number_of_passengers=4,
        drive_type=DriveType.FRONT,
        number_of_airbags=8,
        price_per_day=Decimal("99.99"),
    )
    return car_create_dto


def create_test_car(db: Session) -> models.Car:
    car_create_dto = get_test_car_create_dto()
    return services.car.create(db=db, obj_in=car_create_dto)
