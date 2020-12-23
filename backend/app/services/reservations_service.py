from datetime import datetime
from typing import List, Union

from sqlalchemy.orm import Session

from app import services
from app.exceptions.instance_not_found import ReservationNotFoundException
from app.exceptions.rental import RentalCollisionException
from app.exceptions.reservation import (
    CancelReservationWithRentalException,
    ReservationCollisionException,
    ReservationCreatedInThePastException,
    UpdatingCancelledReservationException,
    UpdatingCollectedReservationException,
)
from app.models.rental import Rental
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.reservation import ReservationCreateDto, ReservationUpdateDto
from app.services.base import BaseService
from app.utils.interval import Interval
from app.validators.general import (
    is_date_in_the_past,
    validate_start_date_before_end_date,
)


class ReservationService(
    BaseService[Reservation, ReservationCreateDto, ReservationUpdateDto]
):
    def validate_start_date_in_future(
        self, start_date: datetime
    ) -> None:
        """
        Start date has to be in the future
        """
        if is_date_in_the_past(start_date):
            raise ReservationCreatedInThePastException()

    # TODO PLEASE REFACTOR
    def validate_collisions(
        self,
        db: Session,
        _reservation: Union[ReservationCreateDto, ReservationUpdateDto, Reservation],
        current_reservation_id: int = None,
    ) -> None:
        reservations_for_this_car = self.get_active_by_car_id(db, _reservation.car_id)
        reservation_timeframe = Interval(_reservation.start_date, _reservation.end_date)

        for other_reservation in reservations_for_this_car:
            if (
                current_reservation_id
                and current_reservation_id == other_reservation.id
            ):
                # collision with the same object is obvious, skip
                continue

            other_reservation_timeframe = Interval(
                other_reservation.start_date, other_reservation.end_date
            )
            if reservation_timeframe.is_intersecting(other_reservation_timeframe):
                raise ReservationCollisionException()

        rentals_for_this_car = services.rental.get_active_by_car_id(
            db=db, car_id=_reservation.car_id
        )
        for other_rental in rentals_for_this_car:
            other_rental_timeframe = Interval(
                other_rental.start_date, other_rental.end_date
            )
            if reservation_timeframe.is_intersecting(other_rental_timeframe):
                raise RentalCollisionException()

        # TODO probably move to other module since this will be used in many places

    def validate_old_status_on_update(
        self, old_status: ReservationStatus
    ) -> None:
        """
        Cannot update reservations that is cancelled or collected
        """
        if old_status == ReservationStatus.CANCELLED:
            raise UpdatingCancelledReservationException()
        if old_status == ReservationStatus.COLLECTED:
            raise UpdatingCollectedReservationException()

    def validate_rental_relation(
        self,
        old_status: ReservationStatus,
        new_status: ReservationStatus,
        rental: Rental,
    ) -> None:
        """
        Cannot cancel reservation that has related rental
        """
        if (
            rental
            and old_status != ReservationStatus.CANCELLED
            and new_status == ReservationStatus.CANCELLED
        ):
            raise CancelReservationWithRentalException()

    def create(self, db: Session, *, obj_in: ReservationCreateDto) -> Reservation:
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_collisions(db, obj_in)
        self.validate_start_date_in_future(obj_in.start_date)

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Reservation, obj_in: ReservationUpdateDto
    ) -> Reservation:
        self.validate_old_status_on_update(db_obj.status)  # type: ignore
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_collisions(db, obj_in, db_obj.id)
        self.validate_rental_relation(
            db_obj.status,  # type: ignore
            obj_in.status,
            db_obj.rental,  # type: ignore
        )

        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def mark_collected(self, db: Session, reservation_id: int) -> Reservation:
        return self._update_status(db, reservation_id, ReservationStatus.COLLECTED)

    def mark_cancelled(self, db: Session, reservation_id: int) -> Reservation:
        return self._update_status(db, reservation_id, ReservationStatus.CANCELLED)

    def _update_status(
        self, db: Session, reservation_id: int, status: ReservationStatus
    ) -> Reservation:
        _reservation = self.get(db=db, _id=reservation_id)
        if not _reservation:
            raise ReservationNotFoundException()

        reservation_update_dto = ReservationUpdateDto(
            car_id=_reservation.car_id,
            customer_id=_reservation.customer_id,
            start_date=_reservation.start_date,
            end_date=_reservation.end_date,
            status=status,
        )
        return self.update(db=db, db_obj=_reservation, obj_in=reservation_update_dto)

    def get_active_by_car_id(self, db: Session, car_id: int) -> List[Reservation]:
        return (
            db.query(Reservation)
            .filter(
                Reservation.car_id == car_id,
                Reservation.status == ReservationStatus.NEW,
            )
            .all()
        )

    def get_active(self, db: Session) -> List[Reservation]:
        return (
            db.query(Reservation)
            .filter(Reservation.status == ReservationStatus.NEW)
            .all()
        )

    def get_missed_reservations(self, db: Session) -> List[Reservation]:
        now = datetime.now()
        return (
            db.query(Reservation)
            .filter(
                Reservation.status == ReservationStatus.NEW,
                Reservation.start_date < now,
            )
            .all()
        )

    def cancel_missed_reservations(self, db: Session) -> None:
        missed_reservations = self.get_missed_reservations(db)
        for _reservation in missed_reservations:
            self.mark_cancelled(db, _reservation.id)


reservation = ReservationService(Reservation)
