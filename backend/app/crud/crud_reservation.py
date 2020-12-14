from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreateDto, ReservationUpdateDto


class CRUDReservation(CRUDBase[Reservation, ReservationCreateDto, ReservationUpdateDto]):
    pass


reservation = CRUDReservation(Reservation)
