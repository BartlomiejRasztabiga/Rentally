from datetime import datetime

from sqlalchemy.orm import Session

from app import services
from app.models import Reservation
from app.models.car import Car
from app.models.customer import Customer
from app.models.reservation import ReservationStatus
from app.schemas.reservation import ReservationCreateDto


def get_test_reservation_create_dto(
    car: Car,
    customer: Customer,
    start_date: datetime,
    end_date: datetime,
    status: ReservationStatus = ReservationStatus.NEW,
) -> ReservationCreateDto:
    reservation_create_dto = ReservationCreateDto(
        car_id=car.id,
        customer_id=customer.id,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    return reservation_create_dto


def create_test_reservation(
    db: Session,
    car: Car,
    customer: Customer,
    start_date: datetime,
    end_date: datetime,
    status: ReservationStatus = ReservationStatus.NEW,
) -> Reservation:
    reservation_create_dto = get_test_reservation_create_dto(
        car, customer, start_date, end_date, status
    )
    return services.reservation.create(db=db, obj_in=reservation_create_dto)
