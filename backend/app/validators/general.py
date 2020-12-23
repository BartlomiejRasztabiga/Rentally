from typing import Optional

from sqlalchemy.orm import Session

from app import services
from app.exceptions.instance_not_found import (
    CarNotFoundException,
    CustomerNotFoundException,
    ReservationNotFoundException,
)


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
