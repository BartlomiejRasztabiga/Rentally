from app.crud.base import CRUDBase
from app.models import Truck
from app.schemas.truck import TruckUpdateDto, TruckCreateDto


class CRUDTruck(CRUDBase[Truck, TruckCreateDto, TruckUpdateDto]):
    pass


truck = CRUDTruck(Truck)
