from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy.orm import Session

from app import services
from app.exceptions.instance_not_found import (
    CarNotFoundException,
    CustomerNotFoundException,
    ReservationNotFoundException,
)
from app.exceptions.reservation import StartDateNotBeforeEndDateException
from app.utils.datetime_utils import datetime_without_seconds


def validate_car_with_id_exists(db: Session, car_id: int) -> None:
    car = services.car.get(db=db, _id=car_id)
    if not car:
        raise CarNotFoundException()


def validate_customer_with_id_exists(db: Session, customer_id: int) -> None:
    customer = services.customer.get(db=db, _id=customer_id)
    if not customer:
        raise CustomerNotFoundException()


def validate_reservation_with_id_exists(
    db: Session, reservation_id: Optional[int] = None
) -> None:
    if reservation_id:
        reservation = services.reservation.get(db=db, _id=reservation_id)
        if not reservation:
            raise ReservationNotFoundException()


def validate_start_date_before_end_date(
    start_date: datetime, end_date: datetime
) -> None:
    delta = end_date - start_date
    if delta.total_seconds() <= 0:
        raise StartDateNotBeforeEndDateException()


def is_date_in_the_past(date: datetime) -> bool:
    now = datetime.now(tz=pytz.UTC)
    now_without_seconds = datetime_without_seconds(now)
    start_date_without_seconds = datetime_without_seconds(date)
    return start_date_without_seconds < now_without_seconds
