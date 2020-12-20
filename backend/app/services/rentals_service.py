from copy import deepcopy
from datetime import datetime
from typing import List, Union

import pytz
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import services
from app.exceptions.rental import (
    RentalAndReservationDifferenceException,
    RentalCollisionException,
    RentalCreatedInThePastException,
    UpdatingCompletedRentalException,
)
from app.exceptions.reservation import (
    ReservationCollisionException,
    StartDateNotBeforeEndDateException,
)
from app.models import Rental
from app.models.rental import RentalStatus
from app.schemas.rental import RentalCreateDto, RentalUpdateDto
from app.services.base import BaseService
from app.utils.datetime_utils import datetime_without_seconds
from app.utils.interval import Interval


class RentalService(BaseService[Rental, RentalCreateDto, RentalUpdateDto]):
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
            raise RentalCreatedInThePastException()

    @staticmethod
    def validate_sync_with_reservation(
        db: Session, _rental: Union[RentalCreateDto, RentalUpdateDto, Rental]
    ) -> None:
        if _rental.reservation_id:
            _reservation = services.reservation.get(db=db, _id=_rental.reservation_id)
            # was created from reservation, has to maintain same car_id and customer_id
            # as the reservation it was created from
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

    @staticmethod
    def validate_status(old_status: RentalStatus, new_status: RentalStatus) -> None:
        if old_status == RentalStatus.COMPLETED:
            raise UpdatingCompletedRentalException()

    def create(self, db: Session, *, obj_in: RentalCreateDto) -> Rental:
        self.validate_dates(obj_in.start_date, obj_in.end_date)

        self.validate_collisions(db, obj_in)

        self.validate_dates_on_create(obj_in.start_date, obj_in.end_date)
        self.validate_sync_with_reservation(db, obj_in)

        # update reservation status to COLLECTED
        if obj_in.reservation_id:
            services.reservation.mark_collected(
                db=db, reservation_id=obj_in.reservation_id
            )

        obj_in.status = RentalStatus.IN_PROGRESS
        return super().create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Rental, obj_in: RentalUpdateDto) -> Rental:
        old_rental = deepcopy(db_obj)

        # update db_obj
        # TODO extract
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.validate_status(old_rental.status, obj_in.status)  # type: ignore
        self.validate_dates(db_obj.start_date, db_obj.end_date)
        self.validate_collisions(db, db_obj, db_obj.id)
        self.validate_sync_with_reservation(db, db_obj)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active_by_car_id(self, db: Session, car_id: int) -> List[Rental]:
        return (
            db.query(Rental)
            .filter(Rental.car_id == car_id, Rental.status == RentalStatus.IN_PROGRESS,)
            .all()
        )

    def get_active(self, db: Session) -> List[Rental]:
        return db.query(Rental).filter(Rental.status == RentalStatus.IN_PROGRESS,).all()

    def get_overtime(self, db: Session) -> List[Rental]:
        now = datetime.now()
        return (
            db.query(Rental)
            .filter(Rental.status == RentalStatus.IN_PROGRESS, Rental.end_date < now,)
            .all()
        )


rental = RentalService(Rental)
