from app.crud.base import CRUDBase
from app.models.car import Car
from app.schemas.car import CarCreateDto, CarUpdateDto


class CRUDCar(CRUDBase[Car, CarCreateDto, CarUpdateDto]):
    pass


car = CRUDCar(Car)
