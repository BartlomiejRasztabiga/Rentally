from decimal import Decimal

from sqlalchemy.orm import Session

from app import services
from app.models.car import AcType, CarType, DriveType, FuelType, GearboxType
from app.schemas import CarCreateDto, CarUpdateDto
from app.schemas.cars_search_query import (
    AvailabilityDatesRange,
    CarsSearchQuery,
    NumberOfPassengersRange,
    PricePerDayRange,
)
from app.tests.utils.car import create_test_car, get_test_car_create_dto
from app.tests.utils.customer import create_test_customer
from app.tests.utils.rental import create_test_rental
from app.tests.utils.reservation import create_test_reservation
from app.tests.utils.utils import get_datetime


def test_create_car(db: Session) -> None:
    car_create_dto = get_test_car_create_dto()
    car = services.car.create(db=db, obj_in=car_create_dto)

    assert car.type == car_create_dto.type
    assert car.price_per_day == car_create_dto.price_per_day
    assert car.model_name == car_create_dto.model_name
    assert car.id is not None


def test_get_car(db: Session) -> None:
    car = create_test_car(db)

    stored_car = services.car.get(db=db, _id=car.id)

    assert stored_car
    assert stored_car.type == car.type
    assert stored_car.price_per_day == car.price_per_day
    assert stored_car.model_name == car.model_name
    assert stored_car.id is not None


def test_update_car(db: Session) -> None:
    car = create_test_car(db)

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
    car = create_test_car(db)

    deleted_car = services.car.remove(db=db, _id=car.id)
    car_after_delete = services.car.get(db=db, _id=car.id)

    assert car_after_delete is None
    assert deleted_car.id == car.id
    assert deleted_car.price_per_day == car.price_per_day
    assert deleted_car.model_name == car.model_name


def test_search_query(db: Session) -> None:
    car1 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.CAR,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=4,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("99.99"),
        ),
    )

    truck1 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.TRUCK,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=4,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("99.99"),
        ),
    )

    truck2 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.TRUCK,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=12,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("99.99"),
        ),
    )

    truck3 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.TRUCK,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=2,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("99.99"),
        ),
    )

    truck4 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.TRUCK,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=2,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("99.99"),
        ),
    )

    truck5 = services.car.create(
        db,
        obj_in=CarCreateDto(
            model_name="test",
            type=CarType.TRUCK,
            fuel_type=FuelType.DIESEL,
            gearbox_type=GearboxType.AUTO,
            ac_type=AcType.AUTO,
            number_of_passengers=2,
            drive_type=DriveType.FRONT,
            number_of_airbags=8,
            price_per_day=Decimal("150"),
        ),
    )

    query = CarsSearchQuery()
    query.model_name = "TES"
    query.type = CarType.TRUCK
    query.number_of_passengers = NumberOfPassengersRange(start=1, end=5)
    query.price_per_day = PricePerDayRange(start=50.0, end=100.0)

    found_cars = services.car.get_by_criteria(db, query)
    found_ids = [car.id for car in found_cars]

    assert truck1.id in found_ids
    assert truck2.id not in found_ids
    assert truck3.id in found_ids
    assert truck4.id in found_ids
    assert truck5.id not in found_ids
    assert car1.id not in found_ids


def test_get_by_criteria_availability(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    start_date2 = get_datetime(2030, 12, 3)
    end_date2 = get_datetime(2030, 12, 4)

    create_test_reservation(db, car, customer, start_date1, end_date1)
    create_test_rental(db, car, customer, start_date2, end_date2)

    query = CarsSearchQuery()
    query.availability_dates = AvailabilityDatesRange(start=start_date1, end=end_date2)

    available_cars = services.car.get_by_criteria(db, query)
    assert car.id not in [car.id for car in available_cars]
