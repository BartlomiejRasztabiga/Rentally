from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import services
from app.models.car import Car
from app.schemas.car import CarCreateDto, CarUpdateDto
from app.schemas.cars_search_query import AvailabilityDatesRange, CarsSearchQuery
from app.services.base import BaseService
from app.utils.interval import Interval


class CarService(BaseService[Car, CarCreateDto, CarUpdateDto]):
    def get_by_criteria(
        self, db: Session, cars_search_query: CarsSearchQuery
    ) -> List[Car]:
        conditions = cars_search_query.to_conditions()
        found_cars = db.query(Car).filter(and_(*conditions)).all()

        availability_dates = cars_search_query.availability_dates
        found_cars = self._filter_by_availability_dates(
            db, found_cars, availability_dates
        )

        return found_cars

    def _filter_by_availability_dates(
        self,
        db: Session,
        cars: List[Car],
        availability_dates: Optional[AvailabilityDatesRange],
    ) -> List[Car]:
        if availability_dates:
            cars = [
                _car
                for _car in cars
                if self._is_available_in_dates(
                    db, _car.id, availability_dates.start, availability_dates.end
                )
            ]
        return cars

    def _is_available_in_dates(
        self, db: Session, car_id: int, start_date: datetime, end_date: datetime
    ) -> bool:
        available = True
        timeframe = Interval(start_date, end_date)

        # check rentals
        rentals_for_this_car = services.rental.get_active_by_car_id(db, car_id)
        for other_rental in rentals_for_this_car:
            other_rental_timeframe = Interval(
                other_rental.start_date, other_rental.end_date
            )
            if timeframe.is_intersecting(other_rental_timeframe):
                available = False
                break

        # check reservations
        reservations_for_this_car = services.reservation.get_active_by_car_id(
            db, car_id
        )
        for other_reservation in reservations_for_this_car:
            other_reservation_timeframe = Interval(
                other_reservation.start_date, other_reservation.end_date
            )
            if timeframe.is_intersecting(other_reservation_timeframe):
                available = False
                break

        return available


car = CarService(Car)
