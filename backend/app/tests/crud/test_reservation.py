from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app import crud
from app.exceptions.reservation import (
    InvalidStatusTransitionReservationException,
    ReservationCollisionException,
    StartDateNotBeforeEndDateException,
    UpdatingCancelledReservationException,
)
from app.models.reservation import ReservationStatus
from app.schemas import ReservationUpdateDto
from app.tests.utils.car import create_random_car
from app.tests.utils.customer import create_random_customer
from app.tests.utils.reservation import get_test_reservation_create_dto


def test_create_reservation(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1, 9, 0)
    end_date = datetime(2020, 12, 2, 12, 0)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    assert reservation.id is not None
    assert reservation.start_date == start_date
    assert reservation.end_date == end_date
    assert reservation.status == ReservationStatus.NEW
    assert reservation.car == car
    assert reservation.customer == customer


def test_create_reservation_wrong_dates(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 2)
    end_date = datetime(2020, 12, 1)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date
    )
    with pytest.raises(StartDateNotBeforeEndDateException):
        crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_wrong_dates2(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1, 9, 0)
    end_date = datetime(2020, 12, 1, 9, 0)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date
    )
    with pytest.raises(StartDateNotBeforeEndDateException):
        crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_same_car_same_dates_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 1, 9)
    end_date1 = datetime(2020, 12, 2, 12)

    start_date2 = datetime(2020, 12, 1, 11)
    end_date2 = datetime(2020, 12, 2, 15)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    with pytest.raises(ReservationCollisionException):
        crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_same_car_one_day_intersection_will_throw(
    db: Session,
) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 1, 9)
    end_date1 = datetime(2020, 12, 5, 12)

    start_date2 = datetime(2020, 12, 5, 17)
    end_date2 = datetime(2020, 12, 7, 15)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    with pytest.raises(ReservationCollisionException):
        crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_same_car_one_day_intersection_will_throw2(
    db: Session,
) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 5, 9)
    end_date1 = datetime(2020, 12, 9, 12)

    start_date2 = datetime(2020, 12, 2, 9)
    end_date2 = datetime(2020, 12, 5, 7)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    with pytest.raises(ReservationCollisionException):
        crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_same_car_different_intervals(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 5, 9)
    end_date1 = datetime(2020, 12, 9, 12)

    start_date2 = datetime(2020, 12, 10, 3)
    end_date2 = datetime(2020, 12, 15, 7)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_create_reservation_with_custom_status_will_default_to_new(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1)
    end_date = datetime(2020, 12, 2)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date, status=ReservationStatus.COLLECTED
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    assert reservation.id is not None
    assert reservation.start_date == start_date
    assert reservation.end_date == end_date
    assert reservation.status == ReservationStatus.NEW
    assert reservation.car == car
    assert reservation.customer == customer


def test_get_reservation(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1)
    end_date = datetime(2020, 12, 2)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date, status=ReservationStatus.COLLECTED
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    stored_reservation = crud.reservation.get(db=db, _id=reservation.id)

    assert stored_reservation
    assert stored_reservation.start_date == reservation_create_dto.start_date
    assert stored_reservation.end_date == reservation_create_dto.end_date
    assert stored_reservation.status == reservation_create_dto.status
    assert stored_reservation.id is not None


def test_update_reservation(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date = datetime(2020, 12, 1)
    end_date = datetime(2020, 12, 2)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date, status=ReservationStatus.NEW
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.COLLECTED,
    )

    stored_reservation = crud.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    assert stored_reservation
    assert stored_reservation.start_date == reservation_create_dto.start_date
    assert stored_reservation.end_date == reservation_create_dto.end_date
    assert stored_reservation.status == ReservationStatus.COLLECTED
    assert stored_reservation.id is not None


def test_update_reservation_dates_collision_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 3, 9)
    end_date1 = datetime(2020, 12, 4, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )

    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    start_date2 = datetime(2020, 12, 1, 9)
    end_date2 = datetime(2020, 12, 2, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=start_date1,
        end_date=end_date1,
        status=ReservationStatus.COLLECTED,
    )

    with pytest.raises(ReservationCollisionException):
        crud.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_create_reservation_dates_collision_on_cancelled(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 3, 9)
    end_date1 = datetime(2020, 12, 4, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )

    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    crud.reservation.update(db=db, db_obj=reservation, obj_in=reservation_update_dto)

    start_date2 = datetime(2020, 12, 3, 9)
    end_date2 = datetime(2020, 12, 4, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)


def test_update_reservation_cancelled_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 3, 9)
    end_date1 = datetime(2020, 12, 4, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )

    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    crud.reservation.update(db=db, db_obj=reservation, obj_in=reservation_update_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date + timedelta(days=1),
        status=ReservationStatus.CANCELLED,
    )

    with pytest.raises(UpdatingCancelledReservationException):
        crud.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_update_reservation_collected_to_new_will_throw(db: Session) -> None:
    car = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 3, 9)
    end_date1 = datetime(2020, 12, 4, 12)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )

    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.COLLECTED,
    )

    crud.reservation.update(db=db, db_obj=reservation, obj_in=reservation_update_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date + timedelta(days=1),
        status=ReservationStatus.NEW,
    )

    with pytest.raises(InvalidStatusTransitionReservationException):
        crud.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_get_active_by_car_id(db: Session) -> None:
    car1 = create_random_car(db)
    car2 = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 1)
    end_date1 = datetime(2020, 12, 2)

    start_date2 = datetime(2020, 12, 3)
    end_date2 = datetime(2020, 12, 4)

    reservation_create_dto = get_test_reservation_create_dto(
        car1, customer, start_date1, end_date1, status=ReservationStatus.NEW
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car2, customer, start_date2, end_date2, status=ReservationStatus.NEW
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    active_reservations = crud.reservation.get_active_by_car_id(db, car2.id)
    assert len(active_reservations) == 1


def test_get_active_by_car_id_only_active(db: Session) -> None:
    car1 = create_random_car(db)
    customer = create_random_customer(db)

    start_date1 = datetime(2020, 12, 1)
    end_date1 = datetime(2020, 12, 2)

    reservation_create_dto = get_test_reservation_create_dto(
        car1, customer, start_date1, end_date1, status=ReservationStatus.NEW
    )
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    crud.reservation.update(db=db, db_obj=reservation, obj_in=reservation_update_dto)

    active_reservations = crud.reservation.get_active_by_car_id(db, car1.id)
    assert len(active_reservations) == 0


def test_get_active(db: Session) -> None:
    car = create_random_car(db)
    car2 = create_random_car(db)
    customer = create_random_customer(db)
    customer2 = create_random_customer(db)

    start_date1 = datetime(2020, 12, 1)
    end_date1 = datetime(2020, 12, 2)

    start_date2 = datetime(2020, 12, 3)
    end_date2 = datetime(2020, 12, 4)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date1, end_date1
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date2, end_date2
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    reservation_create_dto = get_test_reservation_create_dto(
        car2, customer2, start_date2, end_date2
    )
    crud.reservation.create(db=db, obj_in=reservation_create_dto)

    active_reservations = crud.reservation.get_active(db)
    assert len(active_reservations) >= 3  # there might be other objects in db
