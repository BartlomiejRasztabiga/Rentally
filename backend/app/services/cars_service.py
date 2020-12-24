from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.car import Car
from app.schemas.car import CarCreateDto, CarUpdateDto
from app.schemas.cars_search_query import AvailabilityDatesRange, CarsSearchQuery
from app.services.base import BaseService
from app.validators.availability import is_car_available_in_dates


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
                if is_car_available_in_dates(
                    db, _car.id, availability_dates.start, availability_dates.end
                )
            ]
        return cars


car = CarService(Car)
