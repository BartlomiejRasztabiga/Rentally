from app.services.base import BaseService
from app.models.car import Car
from app.schemas.car import CarCreateDto, CarUpdateDto


class CarService(BaseService[Car, CarCreateDto, CarUpdateDto]):
    pass


car = CarService(Car)
