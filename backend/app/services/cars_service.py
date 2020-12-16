from app.models.car import Car
from app.schemas.car import CarCreateDto, CarUpdateDto
from app.services.base import BaseService


class CarService(BaseService[Car, CarCreateDto, CarUpdateDto]):
    pass


car = CarService(Car)
