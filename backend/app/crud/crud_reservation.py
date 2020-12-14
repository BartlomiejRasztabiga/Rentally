from datetime import datetime
from typing import List, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.exceptions.reservation import (
    ReservationCollisionException,
    StartDateNotBeforeEndDateException,
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
    ) -> None:
        reservations_for_this_car = self.get_active_by_car_id(db, obj.car_id)
        interval1 = Interval(obj.start_date, obj.end_date)

        for _reservation in reservations_for_this_car:
            interval2 = Interval(_reservation.start_date, _reservation.end_date)
            if interval1.is_intersecting(interval2):
                raise ReservationCollisionException()

        # TODO do the same for Rentals

    def create(self, db: Session, *, obj_in: ReservationCreateDto) -> Reservation:
        self.validate_dates(obj_in.start_date, obj_in.end_date)

        # TODO cannot reserve a car if there is already another reservation
        # or rental for the same time frame
        self.validate_collisions(db, obj_in)

        obj_in.status = ReservationStatus.NEW
        return super().create(db=db, obj_in=obj_in)

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
