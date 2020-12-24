from datetime import datetime, timedelta

import pytest
import pytz
from sqlalchemy.orm import Session

from app import services
from app.exceptions.rental import (
    RentalAndReservationDifferenceException,
    RentalCollisionException,
    RentalCreatedInThePastException,
    UpdatingCompletedRentalException,
)
from app.exceptions.reservation import (
    ReservationCollisionException,
    StartDateNotBeforeEndDateException,
)
from app.models.rental import RentalStatus
from app.schemas.rental import RentalUpdateDto
from app.tests.utils.car import create_test_car
from app.tests.utils.customer import create_test_customer
from app.tests.utils.rental import create_test_rental
from app.tests.utils.reservation import create_test_reservation
from app.tests.utils.utils import get_datetime


def test_create_standalone_rental(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 2, 12, 0)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    assert rental.id is not None
    assert rental.start_date == start_date
    assert rental.end_date == end_date
    assert rental.status == RentalStatus.IN_PROGRESS
    assert rental.reservation is None
    assert rental.car == car
    assert rental.customer == customer


def test_create_rental_with_reservation(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 2, 12, 0)

    reservation = create_test_reservation(db, car, customer, start_date, end_date)

    rental = create_test_rental(
        db, car, customer, start_date, end_date, reservation=reservation
    )

    assert rental.id is not None
    assert rental.start_date == start_date
    assert rental.end_date == end_date
    assert rental.status == RentalStatus.IN_PROGRESS
    assert rental.reservation is not None
    assert rental.car == car
    assert rental.customer == customer


def test_update_rental_with_reservation_change_carid_customerid_will_throw(
    db: Session,
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)
    car1 = create_test_car(db)
    customer2 = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 2, 12, 0)

    reservation = create_test_reservation(db, car, customer, start_date, end_date)

    rental = create_test_rental(
        db, car, customer, start_date, end_date, reservation=reservation
    )

    rental_update_dto = RentalUpdateDto(
        car_id=car1.id,
        customer_id=customer2.id,
        reservation_id=rental.reservation_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=rental.status,
    )

    with pytest.raises(RentalAndReservationDifferenceException):
        services.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)


def test_update_completed_rental_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 2, 12, 0)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    services.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date + timedelta(days=1),
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    with pytest.raises(UpdatingCompletedRentalException):
        services.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)


def test_create_rental_in_the_past_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2020, 12, 1, 9, 0)
    end_date = get_datetime(2020, 12, 2, 12, 0)

    with pytest.raises(RentalCreatedInThePastException):
        create_test_rental(db, car, customer, start_date, end_date)


def test_create_rental_end_before_start_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 2, 9, 0)
    end_date = get_datetime(2030, 12, 1, 12, 0)

    with pytest.raises(StartDateNotBeforeEndDateException):
        create_test_rental(db, car, customer, start_date, end_date)


def test_get_active(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 12, 0)
    end_date = get_datetime(2030, 12, 2, 9, 0)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    updated_rental = services.rental.update(
        db=db, db_obj=rental, obj_in=rental_update_dto
    )

    active_rentals = services.rental.get_active(db=db)

    assert updated_rental not in active_rentals


def test_create_rental_collision_with_another_rental_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1)
    end_date = get_datetime(2030, 12, 2)

    create_test_rental(db, car, customer, start_date, end_date)

    with pytest.raises(RentalCollisionException):
        create_test_rental(db, car, customer, start_date, end_date)


def test_create_rental_collision_with_reservation_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1)
    end_date = get_datetime(2030, 12, 2)

    create_test_reservation(db, car, customer, start_date, end_date)

    with pytest.raises(ReservationCollisionException):
        create_test_rental(db, car, customer, start_date, end_date)


def test_get_overtime_rentals(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = datetime.now(tz=pytz.UTC)
    end_date1 = datetime.now(tz=pytz.UTC) + timedelta(milliseconds=1)

    rental = create_test_rental(db, car, customer, start_date1, end_date1)

    overtime = services.rental.get_overtime(db)
    assert rental.id in [rental.id for rental in overtime]


def test_get_overtime_rentals_no_overtime(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = datetime.now(tz=pytz.UTC)
    end_date1 = datetime.now(tz=pytz.UTC) + timedelta(days=1)

    rental = create_test_rental(db, car, customer, start_date1, end_date1)

    overtime = services.rental.get_overtime(db)
    assert rental.id not in [rental.id for rental in overtime]
