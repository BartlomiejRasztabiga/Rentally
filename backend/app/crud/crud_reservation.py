from copy import deepcopy
from datetime import datetime
from typing import List, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.exceptions.reservation import (
    InvalidStatusTransitionReservationException,
    ReservationCollisionException,
    StartDateNotBeforeEndDateException,
    UpdatingCancelledReservationException,
)
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.reservation import ReservationCreateDto, ReservationUpdateDto
from app.utils.interval import Interval


class CRUDReservation(
    CRUDBase[Reservation, ReservationCreateDto, ReservationUpdateDto]
):
    @staticmethod
    def validate_dates(start_date: datetime, end_date: datetime) -> None:
        delta = end_date - start_date
        if delta.total_seconds() <= 0:
            raise StartDateNotBeforeEndDateException()

    def validate_collisions(
        self,
        db: Session,
        obj: Union[ReservationCreateDto, ReservationUpdateDto, Reservation],
        current_reservation_id: int = None,
    ) -> None:
        reservations_for_this_car = self.get_active_by_car_id(db, obj.car_id)
        interval1 = Interval(obj.start_date, obj.end_date)

        for _reservation in reservations_for_this_car:
            if current_reservation_id and current_reservation_id == _reservation.id:
                # collision with the same object is obvious, skip
                continue

            interval2 = Interval(_reservation.start_date, _reservation.end_date)
            if interval1.is_intersecting(interval2):
                raise ReservationCollisionException()

        # TODO do the same for Rentals
        # TODO probably move to other module since this will be used in many places

    @staticmethod
    def validate_status(
        old_status: ReservationStatus, new_status: ReservationStatus
    ) -> None:
        if old_status == ReservationStatus.CANCELLED:
            raise UpdatingCancelledReservationException()
        if (
            old_status == ReservationStatus.COLLECTED
            and new_status == ReservationStatus.NEW
        ):
            raise InvalidStatusTransitionReservationException()

    def create(self, db: Session, *, obj_in: ReservationCreateDto) -> Reservation:
        self.validate_dates(obj_in.start_date, obj_in.end_date)

        # TODO cannot reserve a car if there is already another reservation
        # TODO or rental for the same time frame
        self.validate_collisions(db, obj_in)

        # TODO dates cannot be in the past on create?

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Reservation, obj_in: ReservationUpdateDto
    ) -> Reservation:
        old_reservation = deepcopy(db_obj)

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.validate_status(old_reservation.status, obj_in.status)  # type: ignore
        self.validate_dates(db_obj.start_date, db_obj.end_date)
        self.validate_collisions(db, db_obj, db_obj.id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active_by_car_id(self, db: Session, car_id: int) -> List[Reservation]:
        return (
            db.query(Reservation)
            .filter(
                Reservation.car_id == car_id,
                or_(
                    Reservation.status == ReservationStatus.NEW,
                    Reservation.status == ReservationStatus.COLLECTED,
                ),
            )
            .all()
        )

    def get_active(self, db: Session) -> List[Reservation]:
        return (
            db.query(Reservation)
            .filter(
                or_(
                    Reservation.status == ReservationStatus.NEW,
                    Reservation.status == ReservationStatus.COLLECTED,
                )
            )
            .all()
        )


reservation = CRUDReservation(Reservation)
