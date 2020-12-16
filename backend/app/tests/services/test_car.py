from decimal import Decimal

from sqlalchemy.orm import Session

from app import services
from app.models.car import AcType, CarType, DriveType, FuelType, GearboxType
from app.schemas import CarUpdateDto
from app.tests.utils.car import get_test_car_create_dto


def test_create_car(db: Session) -> None:
    car_create_dto = get_test_car_create_dto()
    car = services.car.create(db=db, obj_in=car_create_dto)

    assert car.type == car_create_dto.type
    assert car.price_per_day == car_create_dto.price_per_day
    assert car.model_name == car_create_dto.model_name
    assert car.id is not None


def test_get_car(db: Session) -> None:
    car_create_dto = get_test_car_create_dto()
    car = services.car.create(db=db, obj_in=car_create_dto)

    stored_car = services.car.get(db=db, _id=car.id)

    assert stored_car
    assert stored_car.type == car_create_dto.type
    assert stored_car.price_per_day == car_create_dto.price_per_day
    assert stored_car.model_name == car_create_dto.model_name
    assert stored_car.id is not None


def test_update_car(db: Session) -> None:
    car_create_dto = get_test_car_create_dto()
    car = services.car.create(db=db, obj_in=car_create_dto)

    car_update_dto = CarUpdateDto(
        model_name="test",
        type=CarType.CAR,
        fuel_type=FuelType.DIESEL,
        gearbox_type=GearboxType.AUTO,
        ac_type=AcType.AUTO,
        number_of_passengers=4,
        drive_type=DriveType.FRONT,
        number_of_airbags=8,
        price_per_day=Decimal("99.99"),
        deposit_amount=Decimal("10000"),
    )
    updated_car = services.car.update(db=db, db_obj=car, obj_in=car_update_dto)

    assert car.id == updated_car.id
    assert car.type == updated_car.type
    assert updated_car.deposit_amount is not None
    assert updated_car.deposit_amount == car_update_dto.deposit_amount


def test_delete_car(db: Session) -> None:
    car_create_dto = get_test_car_create_dto()
    car = services.car.create(db=db, obj_in=car_create_dto)

    deleted_car = services.car.remove(db=db, _id=car.id)
    car_after_delete = services.car.get(db=db, _id=car.id)

    assert car_after_delete is None
    assert deleted_car.id == car.id
    assert deleted_car.price_per_day == car_create_dto.price_per_day
    assert deleted_car.model_name == car_create_dto.model_name
