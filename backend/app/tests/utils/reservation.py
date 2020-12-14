from datetime import datetime

from app.models.reservation import ReservationStatus
from app.schemas import Car, Customer
from app.schemas.reservation import ReservationCreateDto


def get_test_reservation_create_dto(car: Car, customer: Customer, start_date: datetime,
                                    end_date: datetime,
                                    status: ReservationStatus = ReservationStatus.NEW) -> ReservationCreateDto:
    reservation_create_dto = ReservationCreateDto(
        car_id=car.id,
        customer_id=customer.id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    return reservation_create_dto
