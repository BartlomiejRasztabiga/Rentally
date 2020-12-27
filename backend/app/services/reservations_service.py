from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

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
from app.validators.availability import (
    is_colliding_with_other_rentals,
    is_colliding_with_other_reservations,
)
from app.validators.general import (
    is_date_in_the_past,
    validate_start_date_before_end_date,
)


class ReservationService(
    BaseService[Reservation, ReservationCreateDto, ReservationUpdateDto]
):
    def validate_start_date_in_future(self, start_date: datetime) -> None:
        """
        Start date has to be in the future
        """
        if is_date_in_the_past(start_date):
            raise ReservationCreatedInThePastException()

    def validate_availability_on_create(
        self, db: Session, _reservation: ReservationCreateDto
    ) -> None:
        """
        Validates that new reservation doesn't collide with other reservation or rental
        """
        reservation_timeframe = Interval(_reservation.start_date, _reservation.end_date)

        if is_colliding_with_other_reservations(
            db, _reservation.car_id, reservation_timeframe
        ):
            raise ReservationCollisionException()

        if is_colliding_with_other_rentals(
            db, _reservation.car_id, reservation_timeframe
        ):
            raise RentalCollisionException()

    def validate_availability_on_update(
        self,
        db: Session,
        _reservation: ReservationUpdateDto,
        current_reservation_id: int = None,
    ) -> None:
        """
        Validates that updated reservation doesn't collide with other reservation (apart from itself) or rental
        """
        reservation_timeframe = Interval(_reservation.start_date, _reservation.end_date)

        if is_colliding_with_other_reservations(
            db, _reservation.car_id, reservation_timeframe, current_reservation_id
        ):
            raise ReservationCollisionException()

        if is_colliding_with_other_rentals(
            db, _reservation.car_id, reservation_timeframe
        ):
            raise RentalCollisionException()

    def validate_old_status_on_update(self, old_status: ReservationStatus) -> None:
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
        """
        Creates new reservation
        """
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_availability_on_create(db, obj_in)
        self.validate_start_date_in_future(obj_in.start_date)

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Reservation, obj_in: ReservationUpdateDto
    ) -> Reservation:
        """
        Updates reservation
        """
        self.validate_old_status_on_update(db_obj.status)  # type: ignore
        validate_start_date_before_end_date(obj_in.start_date, obj_in.end_date)
        self.validate_availability_on_update(db, obj_in, db_obj.id)
        self.validate_rental_relation(
            db_obj.status,  # type: ignore
            obj_in.status,
            db_obj.rental,  # type: ignore
        )

        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def mark_collected(self, db: Session, reservation_id: int) -> Reservation:
        """
        Sets reservation's status to COLLECTED
        """
        return self._update_status(db, reservation_id, ReservationStatus.COLLECTED)

    def mark_cancelled(self, db: Session, reservation_id: int) -> Reservation:
        """
        Sets reservation's status to CANCELLED
        """
        return self._update_status(db, reservation_id, ReservationStatus.CANCELLED)

    def _update_status(
        self, db: Session, reservation_id: int, status: ReservationStatus
    ) -> Reservation:
        """
        Updates reservation's status
        """
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
        """
        Returns all active reservations by car id
        """
        return (
            db.query(Reservation)
            .filter(
                Reservation.car_id == car_id,
                Reservation.status == ReservationStatus.NEW,
            )
            .all()
        )

    def get_active(self, db: Session) -> List[Reservation]:
        """
        Returns all active reservations
        """
        return (
            db.query(Reservation)
            .filter(Reservation.status == ReservationStatus.NEW)
            .all()
        )

    def get_missed(self, db: Session) -> List[Reservation]:
        """
        Returns "missed" (start_date < now) reservations
        """
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
        """
        Cancels all "missed" (start_date < now) reservations
        """
        missed_reservations = self.get_missed(db)
        for _reservation in missed_reservations:
            self.mark_cancelled(db, _reservation.id)


reservation = ReservationService(Reservation)
