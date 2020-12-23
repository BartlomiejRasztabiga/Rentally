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
from app.validators.general import (
    is_date_in_the_past,
    validate_start_date_before_end_date,
)


class RentalService(BaseService[Rental, RentalCreateDto, RentalUpdateDto]):

    def validate_start_date_in_future(
        self, start_date: datetime
    ) -> None:
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

    # TODO PLEASE REFACTOR
    def validate_collisions(
        self,
        db: Session,
        _rental: Union[RentalCreateDto, RentalUpdateDto, Rental],
        current_rental_id: int = None,
    ) -> None:
        reservations_for_this_car = services.reservation.get_active_by_car_id(
            db=db, car_id=_rental.car_id
        )
        rental_timeframe = Interval(_rental.start_date, _rental.end_date)

        for other_reservation in reservations_for_this_car:
            if (
                _rental.reservation_id
                and _rental.reservation_id == other_reservation.id
            ):
                # collision with the same object is obvious, skip
                continue
            other_reservation_timeframe = Interval(
                other_reservation.start_date, other_reservation.end_date
            )
            if rental_timeframe.is_intersecting(other_reservation_timeframe):
                raise ReservationCollisionException()

        rentals_for_this_car = self.get_active_by_car_id(db=db, car_id=_rental.car_id)
        for other_rental in rentals_for_this_car:
            if current_rental_id and current_rental_id == other_rental.id:
                # collision with the same object is obvious, skip
                continue

            other_rental_timeframe = Interval(
                other_rental.start_date, other_rental.end_date
            )
            if rental_timeframe.is_intersecting(other_rental_timeframe):
                raise RentalCollisionException()

        # TODO probably move to other module since this will be used in many places

    def validate_old_status_on_update(
        self, old_status: RentalStatus
    ) -> None:
        """
        Cannot update rental that is completed
        """
        if old_status == RentalStatus.COMPLETED:
            raise UpdatingCompletedRentalException()

    def create(self, db: Session, *, obj_in: RentalCreateDto) -> Rental:
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_collisions(db, obj_in)
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
        self.validate_collisions(db, obj_in, db_obj.id)
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
