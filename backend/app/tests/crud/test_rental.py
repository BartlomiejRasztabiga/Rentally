from datetime import datetime, timedelta

import pytest
import pytz
from sqlalchemy.orm import Session

from app import crud
from app.exceptions.rental import RentalAndReservationDifferenceException, UpdatingCompletedRentalException, \
    RentalCreatedInThePastException, RentalCollisionException
from app.exceptions.reservation import StartDateNotBeforeEndDateException, ReservationCollisionException
from app.models.rental import RentalStatus
from app.schemas.rental import RentalUpdateDto
from app.tests.utils.car import create_random_car
from app.tests.utils.customer import create_random_customer
from app.tests.utils.rental import get_test_rental_create_dto
from app.tests.utils.reservation import create_random_reservation


def test_create_standalone_rental(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2030, 12, 1, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 2, 12, 0, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)

    rental = crud.rental.create(db=db, obj_in=rental_create_dto)

    assert rental.id is not None
    assert rental.start_date == start_date
    assert rental.end_date == end_date
    assert rental.status == RentalStatus.IN_PROGRESS
    assert rental.reservation is None
    assert rental.car == car
    assert rental.customer == customer


def test_create_rental_with_reservation(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2030, 12, 1, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 2, 12, 0, tzinfo=pytz.UTC)

    reservation = create_random_reservation(db, car, customer, start_date, end_date)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date, reservation=reservation)

    rental = crud.rental.create(db=db, obj_in=rental_create_dto)

    assert rental.id is not None
    assert rental.start_date == start_date
    assert rental.end_date == end_date
    assert rental.status == RentalStatus.IN_PROGRESS
    assert rental.reservation is not None
    assert rental.car == car
    assert rental.customer == customer


def test_update_rental_with_reservation_change_carid_customerid_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)
    car1 = create_random_car(db)
    customer2 = create_random_customer(db)

    start_date = datetime(2030, 12, 1, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 2, 12, 0, tzinfo=pytz.UTC)

    reservation = create_random_reservation(db, car, customer, start_date, end_date)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date, reservation=reservation)

    rental = crud.rental.create(db=db, obj_in=rental_create_dto)

    rental_update_dto = RentalUpdateDto(
        car_id=car1.id,
        customer_id=customer2.id,
        reservation_id=rental.reservation_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=rental.status,
    )

    with pytest.raises(RentalAndReservationDifferenceException):
        crud.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)


def test_update_completed_rental_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2030, 12, 1, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 2, 12, 0, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)

    rental = crud.rental.create(db=db, obj_in=rental_create_dto)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    crud.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date + timedelta(days=1),
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    with pytest.raises(UpdatingCompletedRentalException):
        crud.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)


def test_create_rental_in_the_past_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2020, 12, 2, 12, 0, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)

    with pytest.raises(RentalCreatedInThePastException):
        crud.rental.create(db=db, obj_in=rental_create_dto)


def test_create_rental_end_before_start_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2030, 12, 2, 9, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 1, 12, 0, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)

    with pytest.raises(StartDateNotBeforeEndDateException):
        crud.rental.create(db=db, obj_in=rental_create_dto)


def test_get_active(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2030, 12, 1, 12, 0, tzinfo=pytz.UTC)
    end_date = datetime(2030, 12, 2, 9, 0, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)

    rental = crud.rental.create(db=db, obj_in=rental_create_dto)

    rental_update_dto = RentalUpdateDto(
        car_id=rental.car_id,
        customer_id=rental.customer_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=RentalStatus.COMPLETED,
    )

    updated_rental = crud.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)

    active_rentals = crud.rental.get_active(db=db)

    assert updated_rental not in active_rentals


def test_create_rental_collision_with_another_rental_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2030, 12, 1, tzinfo=pytz.UTC)
    end_date1 = datetime(2030, 12, 2, tzinfo=pytz.UTC)

    start_date2 = datetime(2030, 12, 1, tzinfo=pytz.UTC)
    end_date2 = datetime(2030, 12, 2, tzinfo=pytz.UTC)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date1, end_date1)

    crud.rental.create(db=db, obj_in=rental_create_dto)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date2, end_date2)

    with pytest.raises(RentalCollisionException):
        crud.rental.create(db=db, obj_in=rental_create_dto)


def test_create_rental_collision_with_reservation_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2030, 12, 1, tzinfo=pytz.UTC)
    end_date1 = datetime(2030, 12, 2, tzinfo=pytz.UTC)

    create_random_reservation(db, car, customer, start_date1, end_date1)

    rental_create_dto = get_test_rental_create_dto(car, customer, start_date1, end_date1)

    with pytest.raises(ReservationCollisionException):
        crud.rental.create(db=db, obj_in=rental_create_dto)
