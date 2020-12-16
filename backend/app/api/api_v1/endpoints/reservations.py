from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.exceptions.instance_not_found import (
    CarNotFoundException,
    CustomerNotFoundException,
    ReservationNotFoundException,
)
from app.exceptions.not_enough_permissions import NotEnoughPermissionsException
from app.models.reservation import Reservation, ReservationStatus

router = APIRouter()


def _validate_car_id(db: Session, car_id: int) -> None:
    car = crud.car.get(db=db, _id=car_id)
    if not car:
        raise CarNotFoundException()


def _validate_customer_id(db: Session, customer_id: int) -> None:
    customer = crud.customer.get(db=db, _id=customer_id)
    if not customer:
        raise CustomerNotFoundException()


@router.get("/", response_model=List[schemas.Reservation])
def get_all_reservations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[Reservation]:
    """
    Retrieve all active reservations.
    """

    reservations = crud.reservation.get_active(db)
    return reservations


@router.get("/{id}", response_model=schemas.Reservation)
def get_reservation(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Reservation:
    """
    Get reservation by ID.
    """
    reservation = crud.reservation.get(db=db, _id=id)
    if not reservation:
        raise ReservationNotFoundException()

    return reservation


@router.delete("/{id}", response_model=schemas.Reservation)
def delete_reservation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Reservation:
    """
    Delete a reservation.
    """
    reservation = crud.reservation.get(db=db, _id=id)

    if not reservation:
        raise ReservationNotFoundException()
    if not crud.user.is_admin(current_user):
        raise NotEnoughPermissionsException()

    reservation = crud.reservation.remove(db=db, _id=id)
    return reservation


@router.post("/", response_model=schemas.Reservation)
def create_reservation(
    *,
    db: Session = Depends(deps.get_db),
    reservation_create_dto: schemas.ReservationCreateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Reservation:
    """
    Create new reservation.
    """

    _validate_car_id(db=db, car_id=reservation_create_dto.car_id)
    _validate_customer_id(db=db, customer_id=reservation_create_dto.customer_id)

    reservation_create_dto.status = ReservationStatus.NEW
    reservation = crud.reservation.create(db=db, obj_in=reservation_create_dto)
    return reservation


@router.put("/{id}", response_model=schemas.Reservation)
def update_reservation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    reservation_update_dto: schemas.ReservationUpdateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Reservation:
    """
    Update a reservation.
    """
    reservation = crud.reservation.get(db=db, _id=id)

    if not reservation:
        raise ReservationNotFoundException()

    _validate_car_id(db=db, car_id=reservation_update_dto.car_id)
    _validate_customer_id(db=db, customer_id=reservation_update_dto.customer_id)

    reservation = crud.reservation.update(
        db=db, db_obj=reservation, obj_in=reservation_update_dto
    )
    return reservation
