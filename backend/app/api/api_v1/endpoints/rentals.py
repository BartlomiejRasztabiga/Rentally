from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.api import deps
from app.exceptions.instance_not_found import RentalNotFoundException
from app.exceptions.not_enough_permissions import NotEnoughPermissionsException
from app.models import Rental
from app.models.rental import RentalStatus
from app.validators import (
    validate_car_with_id_exists,
    validate_customer_with_id_exists,
    validate_reservation_with_id_exists,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.Rental])
def get_all_rentals(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[Rental]:
    """
    Retrieve all rentals.
    """

    rentals = services.rental.get_all(db)
    return rentals


@router.get("/overtime", response_model=List[schemas.Rental])
def get_overtime_rentals(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[Rental]:
    """
    Retrieve overtime rentals.
    """

    rentals = services.rental.get_overtime(db)
    return rentals


@router.get("/{id}", response_model=schemas.Rental)
def get_rental(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Rental:
    """
    Get rental by ID.
    """
    rental = services.rental.get(db=db, _id=id)
    if not rental:
        raise RentalNotFoundException()

    return rental


@router.delete("/{id}", response_model=schemas.Rental)
def delete_rental(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Rental:
    """
    Delete a rental.
    """
    rental = services.rental.get(db=db, _id=id)

    if not rental:
        raise RentalNotFoundException()
    if not services.user.is_admin(current_user):
        raise NotEnoughPermissionsException()

    rental = services.rental.remove(db=db, _id=id)
    return rental


@router.post("/", response_model=schemas.Rental)
def create_rental(
    *,
    db: Session = Depends(deps.get_db),
    rental_create_dto: schemas.RentalCreateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Rental:
    """
    Create new rental.
    """

    validate_car_with_id_exists(db=db, car_id=rental_create_dto.car_id)
    validate_customer_with_id_exists(db=db, customer_id=rental_create_dto.customer_id)
    validate_reservation_with_id_exists(
        db=db, reservation_id=rental_create_dto.reservation_id
    )

    rental_create_dto.status = RentalStatus.IN_PROGRESS
    rental = services.rental.create(db=db, obj_in=rental_create_dto)
    return rental


@router.put("/{id}", response_model=schemas.Rental)
def update_rental(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    rental_update_dto: schemas.RentalUpdateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Rental:
    """
    Update a rental.
    """
    rental = services.rental.get(db=db, _id=id)

    if not rental:
        raise RentalNotFoundException()

    validate_car_with_id_exists(db=db, car_id=rental_update_dto.car_id)
    validate_customer_with_id_exists(db=db, customer_id=rental_update_dto.customer_id)
    validate_reservation_with_id_exists(
        db=db, reservation_id=rental_update_dto.reservation_id
    )

    rental = services.rental.update(db=db, db_obj=rental, obj_in=rental_update_dto)
    return rental
