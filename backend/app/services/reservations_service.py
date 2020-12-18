from copy import deepcopy
from datetime import datetime
from typing import List, Union

import pytz
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import services
from app.exceptions.instance_not_found import ReservationNotFoundException
from app.exceptions.rental import RentalCollisionException
from app.exceptions.reservation import (
    CancelReservationWithRentalException,
    ReservationCollisionException,
    ReservationCreatedInThePastException,
    StartDateNotBeforeEndDateException,
    UpdatingCancelledReservationException,
    UpdatingCollectedReservationException,
)
from app.models.reservation import Reservation, ReservationStatus
from app.schemas import Rental
from app.schemas.reservation import ReservationCreateDto, ReservationUpdateDto
from app.services.base import BaseService
from app.utils.datetime_utils import datetime_without_seconds
from app.utils.interval import Interval


class ReservationService(
    BaseService[Reservation, ReservationCreateDto, ReservationUpdateDto]
):
    @staticmethod
    def validate_dates(start_date: datetime, end_date: datetime) -> None:
        delta = end_date - start_date
        if delta.total_seconds() <= 0:
            raise StartDateNotBeforeEndDateException()

    @staticmethod
    def validate_dates_on_create(start_date: datetime, end_date: datetime) -> None:
        now = datetime.now(tz=pytz.UTC)
        now_without_seconds = datetime_without_seconds(now)
        start_date_without_seconds = datetime_without_seconds(start_date)
        if start_date_without_seconds < now_without_seconds:
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

    @staticmethod
    def validate_status(
        old_status: ReservationStatus, new_status: ReservationStatus
    ) -> None:
        if old_status == ReservationStatus.CANCELLED:
            raise UpdatingCancelledReservationException()
        if old_status == ReservationStatus.COLLECTED:
            raise UpdatingCollectedReservationException()

    @staticmethod
    def validate_rental_relation(
        old_status: ReservationStatus, new_status: ReservationStatus, rental: Rental
    ) -> None:
        if (
            rental
            and old_status != ReservationStatus.CANCELLED
            and new_status == ReservationStatus.CANCELLED
        ):
            raise CancelReservationWithRentalException()

    def create(self, db: Session, *, obj_in: ReservationCreateDto) -> Reservation:
        self.validate_dates(obj_in.start_date, obj_in.end_date)

        self.validate_collisions(db, obj_in)

        self.validate_dates_on_create(obj_in.start_date, obj_in.end_date)

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Reservation, obj_in: ReservationUpdateDto
    ) -> Reservation:
        old_reservation = deepcopy(db_obj)

        # update db_obj
        # TODO extract
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.validate_status(old_reservation.status, obj_in.status)  # type: ignore
        self.validate_dates(db_obj.start_date, db_obj.end_date)
        self.validate_collisions(db, db_obj, db_obj.id)
        self.validate_rental_relation(old_reservation.status, obj_in.status, db_obj.rental)  # type: ignore

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def mark_collected(self, db: Session, reservation_id: int) -> Reservation:
        _reservation = self.get(db=db, _id=reservation_id)
        if not _reservation:
            raise ReservationNotFoundException()

        reservation_update_dto = ReservationUpdateDto(
            car_id=_reservation.car_id,
            customer_id=_reservation.customer_id,
            start_date=_reservation.start_date,
            end_date=_reservation.end_date,
            status=ReservationStatus.COLLECTED,
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
            .filter(Reservation.status == ReservationStatus.NEW,)
            .all()
        )


reservation = ReservationService(Reservation)
