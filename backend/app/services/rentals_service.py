from datetime import datetime
from typing import List, Union

from sqlalchemy.orm import Session

from app import services
from app.exceptions.rental import (
    RentalAndReservationDifferenceException,
    RentalCollisionException,
    RentalCreatedInThePastException,
    UpdatingCompletedRentalException,
)
from app.exceptions.reservation import ReservationCollisionException
from app.models import Rental
from app.models.rental import RentalStatus
from app.schemas.rental import RentalCreateDto, RentalUpdateDto
from app.services.base import BaseService
from app.utils.interval import Interval
from app.validators.availability import (
    is_colliding_with_other_rentals,
    is_colliding_with_other_reservations,
)
from app.validators.general import (
    is_date_in_the_past,
    validate_start_date_before_end_date,
)


class RentalService(BaseService[Rental, RentalCreateDto, RentalUpdateDto]):
    def validate_start_date_in_future(self, start_date: datetime) -> None:
        """
        Start date has to be in the future
        """
        if is_date_in_the_past(start_date):
            raise RentalCreatedInThePastException()

    def validate_in_sync_with_reservation(
        self, db: Session, _rental: Union[RentalCreateDto, RentalUpdateDto, Rental]
    ) -> None:
        """
        If rental was created from reservation,
        ir has to maintain same car_id and customer_id
        as the reservation it was created from
        """
        if _rental.reservation_id:
            _reservation = services.reservation.get(db=db, _id=_rental.reservation_id)
            if (
                _rental.car_id != _reservation.car_id  # type: ignore
                or _rental.customer_id != _reservation.customer_id  # type: ignore
            ):
                raise RentalAndReservationDifferenceException()

    def validate_availability_on_create(
        self, db: Session, _rental: RentalCreateDto
    ) -> None:
        rental_timeframe = Interval(_rental.start_date, _rental.end_date)

        if is_colliding_with_other_reservations(
            db, _rental.car_id, rental_timeframe, _rental.reservation_id
        ):
            raise ReservationCollisionException()

        if is_colliding_with_other_rentals(db, _rental.car_id, rental_timeframe):
            raise RentalCollisionException()

    def validate_availability_on_update(
        self, db: Session, _rental: RentalUpdateDto, current_rental_id: int = None,
    ) -> None:
        rental_timeframe = Interval(_rental.start_date, _rental.end_date)

        if is_colliding_with_other_reservations(
            db, _rental.car_id, rental_timeframe, _rental.reservation_id
        ):
            raise ReservationCollisionException()

        if is_colliding_with_other_rentals(
            db, _rental.car_id, rental_timeframe, current_rental_id
        ):
            raise RentalCollisionException()

    def validate_old_status_on_update(self, old_status: RentalStatus) -> None:
        """
        Cannot update rental that is completed
        """
        if old_status == RentalStatus.COMPLETED:
            raise UpdatingCompletedRentalException()

    def create(self, db: Session, *, obj_in: RentalCreateDto) -> Rental:
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_availability_on_create(db, obj_in)
        self.validate_start_date_in_future(obj_in.start_date)
        self.validate_in_sync_with_reservation(db, obj_in)

        # update reservation status to COLLECTED
        if obj_in.reservation_id:
            services.reservation.mark_collected(
                db=db, reservation_id=obj_in.reservation_id
            )

        obj_in.status = RentalStatus.IN_PROGRESS
        return super().create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Rental, obj_in: RentalUpdateDto) -> Rental:
        self.validate_old_status_on_update(db_obj.status)  # type: ignore
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_availability_on_update(db, obj_in, db_obj.id)
        self.validate_in_sync_with_reservation(db, obj_in)

        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def get_active_by_car_id(self, db: Session, car_id: int) -> List[Rental]:
        return (
            db.query(Rental)
            .filter(Rental.car_id == car_id, Rental.status == RentalStatus.IN_PROGRESS)
            .all()
        )

    def get_active(self, db: Session) -> List[Rental]:
        return db.query(Rental).filter(Rental.status == RentalStatus.IN_PROGRESS).all()

    def get_overtime(self, db: Session) -> List[Rental]:
        now = datetime.now()
        return (
            db.query(Rental)
            .filter(Rental.status == RentalStatus.IN_PROGRESS, Rental.end_date < now)
            .all()
        )


rental = RentalService(Rental)
