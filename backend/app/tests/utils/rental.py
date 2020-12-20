from datetime import datetime

from sqlalchemy.orm import Session

from app import services
from app.models import Car, Customer, Rental, Reservation
from app.models.rental import RentalStatus
from app.schemas.rental import RentalCreateDto


def get_test_rental_create_dto(
    car: Car,
    customer: Customer,
    start_date: datetime,
    end_date: datetime,
    status: RentalStatus = RentalStatus.IN_PROGRESS,
    reservation: Reservation = None,
) -> RentalCreateDto:
    rental_create_dto = RentalCreateDto(
        car_id=car.id,
        customer_id=customer.id,
        reservation_id=reservation.id if reservation else None,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    return rental_create_dto


def create_rental(
    db: Session, car: Car, customer: Customer, start_date: datetime, end_date: datetime
) -> Rental:
    rental_create_dto = get_test_rental_create_dto(car, customer, start_date, end_date)
    return services.rental.create(db=db, obj_in=rental_create_dto)
