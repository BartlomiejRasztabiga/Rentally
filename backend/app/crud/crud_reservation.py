from datetime import datetime
from typing import List, Union

from fastapi.encoders import jsonable_encoder
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
        reservation_id: int = None,
    ) -> None:
        reservations_for_this_car = self.get_active_by_car_id(db, obj.car_id)
        interval1 = Interval(obj.start_date, obj.end_date)

        for _reservation in reservations_for_this_car:
            # TODO shit code
            if reservation_id and reservation_id == _reservation.id:
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
        # TODO add tests
        if old_status == ReservationStatus.CANCELLED:
            raise UpdatingCancelledReservationException()
        if (
            old_status == ReservationStatus.COLLECTED
            and new_status == ReservationStatus.NEW
        ):
            raise InvalidStatusTransitionReservationException()
        if (
            old_status == ReservationStatus.COLLECTED
            and new_status == ReservationStatus.CANCELLED
        ):
            raise InvalidStatusTransitionReservationException()

    def create(self, db: Session, *, obj_in: ReservationCreateDto) -> Reservation:
        self.validate_dates(obj_in.start_date, obj_in.end_date)

        # TODO cannot reserve a car if there is already another reservation
        # or rental for the same time frame
        self.validate_collisions(db, obj_in)

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Reservation, obj_in: ReservationUpdateDto
    ) -> Reservation:
        self.validate_status(db_obj.status, obj_in.status)
        self.validate_dates(obj_in.start_date, obj_in.end_date)
        self.validate_collisions(db, obj_in, db_obj.id)
        # TODO add tests for collisions on updated

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active_by_car_id(self, db: Session, car_id: int) -> List[Reservation]:
        return (
            db.query(Reservation)
            .filter(
                Reservation.car_id == car_id
                and Reservation.status
                in [ReservationStatus.NEW, ReservationStatus.COLLECTED]
            )
            .all()
        )


reservation = CRUDReservation(Reservation)
