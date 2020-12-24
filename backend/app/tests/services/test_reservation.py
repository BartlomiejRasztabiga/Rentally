from datetime import timedelta

import pytest
from sqlalchemy.orm import Session

from app import services
from app.exceptions.instance_not_found import ReservationNotFoundException
from app.exceptions.rental import RentalCollisionException
from app.exceptions.reservation import (
    ReservationCollisionException,
    ReservationCreatedInThePastException,
    StartDateNotBeforeEndDateException,
    UpdatingCancelledReservationException,
    UpdatingCollectedReservationException,
)
from app.models.reservation import ReservationStatus
from app.schemas import ReservationUpdateDto
from app.tests.utils.car import create_test_car
from app.tests.utils.customer import create_test_customer
from app.tests.utils.rental import create_test_rental
from app.tests.utils.reservation import create_test_reservation
from app.tests.utils.utils import get_datetime


def test_create_reservation(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 2, 12, 0)

    reservation = create_test_reservation(db, car, customer, start_date, end_date)

    assert reservation.id is not None
    assert reservation.start_date == start_date
    assert reservation.end_date == end_date
    assert reservation.status == ReservationStatus.NEW
    assert reservation.car == car
    assert reservation.customer == customer


def test_create_reservation_wrong_dates(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 2)
    end_date = get_datetime(2030, 12, 1)

    with pytest.raises(StartDateNotBeforeEndDateException):
        create_test_reservation(db, car, customer, start_date, end_date)


def test_create_reservation_wrong_dates2(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1, 9, 0)
    end_date = get_datetime(2030, 12, 1, 9, 0)

    with pytest.raises(StartDateNotBeforeEndDateException):
        create_test_reservation(db, car, customer, start_date, end_date)


def test_create_reservation_same_car_same_dates_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1, 9)
    end_date1 = get_datetime(2030, 12, 2, 12)

    start_date2 = get_datetime(2030, 12, 1, 11)
    end_date2 = get_datetime(2030, 12, 2, 15)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    with pytest.raises(ReservationCollisionException):
        create_test_reservation(db, car, customer, start_date2, end_date2)


def test_create_reservation_same_car_one_day_intersection_will_throw(
    db: Session,
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1, 9)
    end_date1 = get_datetime(2030, 12, 5, 12)

    start_date2 = get_datetime(2030, 12, 5, 17)
    end_date2 = get_datetime(2030, 12, 7, 15)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    with pytest.raises(ReservationCollisionException):
        create_test_reservation(db, car, customer, start_date2, end_date2)


def test_create_reservation_in_the_past_will_throw(db: Session,) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2020, 12, 1, 9)
    end_date = get_datetime(2020, 12, 5, 12)

    with pytest.raises(ReservationCreatedInThePastException):
        create_test_reservation(db, car, customer, start_date, end_date)


def test_create_reservation_same_car_one_day_intersection_will_throw2(
    db: Session,
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 5, 9)
    end_date1 = get_datetime(2030, 12, 9, 12)

    start_date2 = get_datetime(2030, 12, 2, 9)
    end_date2 = get_datetime(2030, 12, 5, 7)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    with pytest.raises(ReservationCollisionException):
        create_test_reservation(db, car, customer, start_date2, end_date2)


def test_create_reservation_same_car_different_intervals(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 5, 9)
    end_date1 = get_datetime(2030, 12, 9, 12)

    start_date2 = get_datetime(2030, 12, 10, 3)
    end_date2 = get_datetime(2030, 12, 15, 7)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    create_test_reservation(db, car, customer, start_date2, end_date2)


def test_create_reservation_with_custom_status_will_default_to_new(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1)
    end_date = get_datetime(2030, 12, 2)

    reservation = create_test_reservation(
        db, car, customer, start_date, end_date, status=ReservationStatus.COLLECTED
    )

    assert reservation.id is not None
    assert reservation.start_date == start_date
    assert reservation.end_date == end_date
    assert reservation.status == ReservationStatus.NEW
    assert reservation.car == car
    assert reservation.customer == customer


def test_get_reservation(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1)
    end_date = get_datetime(2030, 12, 2)

    reservation = create_test_reservation(
        db, car, customer, start_date, end_date, status=ReservationStatus.COLLECTED
    )

    stored_reservation = services.reservation.get(db=db, _id=reservation.id)

    assert stored_reservation
    assert stored_reservation.start_date == reservation.start_date
    assert stored_reservation.end_date == reservation.end_date
    assert stored_reservation.status == reservation.status
    assert stored_reservation.id is not None


def test_update_reservation(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 1)
    end_date = get_datetime(2030, 12, 2)

    reservation = create_test_reservation(
        db, car, customer, start_date, end_date, status=ReservationStatus.NEW
    )

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.COLLECTED,
    )

    stored_reservation = services.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    assert stored_reservation
    assert stored_reservation.start_date == reservation.start_date
    assert stored_reservation.end_date == reservation.end_date
    assert stored_reservation.status == ReservationStatus.COLLECTED
    assert stored_reservation.id is not None


def test_update_reservation_dates_collision_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 3, 9)
    end_date1 = get_datetime(2030, 12, 4, 12)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    start_date2 = get_datetime(2030, 12, 1, 9)
    end_date2 = get_datetime(2030, 12, 2, 12)

    reservation = create_test_reservation(db, car, customer, start_date2, end_date2)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=start_date1,
        end_date=end_date1,
        status=ReservationStatus.COLLECTED,
    )

    with pytest.raises(ReservationCollisionException):
        services.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_create_reservation_dates_collision_on_cancelled(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 3, 9)
    end_date1 = get_datetime(2030, 12, 4, 12)

    reservation = create_test_reservation(db, car, customer, start_date1, end_date1)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    services.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    start_date2 = get_datetime(2030, 12, 3, 9)
    end_date2 = get_datetime(2030, 12, 4, 12)

    create_test_reservation(db, car, customer, start_date2, end_date2)


def test_update_reservation_cancelled_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 3, 9)
    end_date1 = get_datetime(2030, 12, 4, 12)

    reservation = create_test_reservation(db, car, customer, start_date1, end_date1)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    services.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date + timedelta(days=1),
        status=ReservationStatus.CANCELLED,
    )

    with pytest.raises(UpdatingCancelledReservationException):
        services.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_update_reservation_collected_to_new_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 3, 9)
    end_date1 = get_datetime(2030, 12, 4, 12)

    reservation = create_test_reservation(db, car, customer, start_date1, end_date1)

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.COLLECTED,
    )

    services.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date + timedelta(days=1),
        status=ReservationStatus.NEW,
    )

    with pytest.raises(UpdatingCollectedReservationException):
        services.reservation.update(
            db=db, db_obj=reservation, obj_in=reservation_update_dto
        )


def test_get_active_by_car_id(db: Session) -> None:
    car1 = create_test_car(db)
    car2 = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    start_date2 = get_datetime(2030, 12, 3)
    end_date2 = get_datetime(2030, 12, 4)

    create_test_reservation(
        db, car1, customer, start_date1, end_date1, status=ReservationStatus.NEW
    )

    create_test_reservation(
        db, car2, customer, start_date2, end_date2, status=ReservationStatus.NEW
    )

    active_reservations = services.reservation.get_active_by_car_id(db, car2.id)
    assert len(active_reservations) == 1


def test_get_active_by_car_id_only_active(db: Session) -> None:
    car1 = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    reservation = create_test_reservation(
        db, car1, customer, start_date1, end_date1, status=ReservationStatus.NEW
    )

    reservation_update_dto = ReservationUpdateDto(
        car_id=reservation.car_id,
        customer_id=reservation.customer_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        status=ReservationStatus.CANCELLED,
    )

    services.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )

    active_reservations = services.reservation.get_active_by_car_id(db, car1.id)
    assert len(active_reservations) == 0


def test_get_active(db: Session) -> None:
    car = create_test_car(db)
    car2 = create_test_car(db)
    customer = create_test_customer(db)
    customer2 = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    start_date2 = get_datetime(2030, 12, 3)
    end_date2 = get_datetime(2030, 12, 4)

    create_test_reservation(db, car, customer, start_date1, end_date1)

    create_test_reservation(db, car, customer, start_date2, end_date2)

    create_test_reservation(db, car2, customer2, start_date2, end_date2)

    active_reservations = services.reservation.get_active(db)
    assert len(active_reservations) >= 3  # there might be other objects in db


def test_create_reservation_collision_with_rental_will_throw(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    start_date2 = get_datetime(2030, 12, 1)
    end_date2 = get_datetime(2030, 12, 2)

    create_test_rental(db, car, customer, start_date1, end_date1)

    with pytest.raises(RentalCollisionException):
        create_test_reservation(db, car, customer, start_date2, end_date2)


def test_mark_reservation_collected(db: Session) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date1 = get_datetime(2030, 12, 1)
    end_date1 = get_datetime(2030, 12, 2)

    reservation = create_test_reservation(db, car, customer, start_date1, end_date1)

    services.reservation.mark_collected(db=db, reservation_id=reservation.id)

    updated_reservation = services.reservation.get(db=db, _id=reservation.id)

    assert updated_reservation
    assert updated_reservation.id == reservation.id
    assert updated_reservation.status == ReservationStatus.COLLECTED


def test_mark_reservation_collected_on_not_existing_will_throw(db: Session) -> None:
    with pytest.raises(ReservationNotFoundException):
        services.reservation.mark_collected(db=db, reservation_id=999999999)
