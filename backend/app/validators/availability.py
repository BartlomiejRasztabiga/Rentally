from datetime import datetime

from sqlalchemy.orm import Session

from app import services
from app.utils.interval import Interval


def is_car_available_in_dates(
        db: Session, car_id: int, start_date: datetime, end_date: datetime, rental_id: int = None,
        reservation_id: int = None
) -> bool:
    available = True
    timeframe = Interval(start_date, end_date)

    if is_colliding_with_other_rentals(db, car_id, timeframe, rental_id):
        available = False

    if is_colliding_with_other_reservations(db, car_id, timeframe, reservation_id):
        available = False

    return available


def is_colliding_with_other_rentals(
        db: Session, car_id: int, timeframe: Interval, rental_id: int = None):
    available = True

    rentals_for_this_car = get_rentals_for_this_car(db, car_id, rental_id)
    for other_rental in rentals_for_this_car:
        other_rental_timeframe = Interval(
            other_rental.start_date, other_rental.end_date
        )
        if timeframe.is_intersecting(other_rental_timeframe):
            available = False
            break

    return not available


def is_colliding_with_other_reservations(
        db: Session, car_id: int, timeframe: Interval, reservation_id: int = None):
    available = True

    reservations_for_this_car = get_reservations_for_this_car(db, car_id, reservation_id)
    for other_reservation in reservations_for_this_car:
        other_reservation_timeframe = Interval(
            other_reservation.start_date, other_reservation.end_date
        )
        if timeframe.is_intersecting(other_reservation_timeframe):
            available = False
            break

    return not available


def get_rentals_for_this_car(db: Session, car_id: int, rental_id: int = None):
    rentals_for_this_car = services.rental.get_active_by_car_id(db, car_id)
    if rental_id:
        rentals_for_this_car = [rental for rental in rentals_for_this_car if rental.id != rental_id]
    return rentals_for_this_car


def get_reservations_for_this_car(db: Session, car_id: int, reservation_id: int = None):
    reservations_for_this_car = services.reservation.get_active_by_car_id(db, car_id)
    if reservation_id:
        reservations_for_this_car = [reservation for reservation in reservations_for_this_car if
                                     reservation.id != reservation_id]
    return reservations_for_this_car
