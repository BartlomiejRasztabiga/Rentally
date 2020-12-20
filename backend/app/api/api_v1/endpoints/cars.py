from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.api import deps
from app.exceptions.instance_not_found import CarNotFoundException
from app.exceptions.not_enough_permissions import NotEnoughPermissionsException
from app.schemas.cars_search_query import CarsSearchQuery

router = APIRouter()


@router.get("/", response_model=List[schemas.Car])
def get_cars(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    cars_search_query: Optional[CarsSearchQuery] = None,
) -> Any:
    """
    Retrieve cars.
    """
    if cars_search_query:
        cars = services.car.get_by_criteria(db, cars_search_query)
    else:
        cars = services.car.get_all(db)

    return cars


@router.get("/{id}", response_model=schemas.Car)
def get_car(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get car by ID.
    """
    car = services.car.get(db=db, _id=id)
    if not car:
        raise CarNotFoundException()

    return car


@router.delete("/{id}", response_model=schemas.Car)
def delete_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a car.
    """
    car = services.car.get(db=db, _id=id)

    if not car:
        raise CarNotFoundException()
    if not services.user.is_admin(current_user):
        raise NotEnoughPermissionsException()

    car = services.car.remove(db=db, _id=id)
    return car


@router.post("/", response_model=schemas.Car)
def create_car(
    *,
    db: Session = Depends(deps.get_db),
    car_create_dto: schemas.CarCreateDto,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new car.
    """
    if not services.user.is_admin(current_user):
        raise NotEnoughPermissionsException()

    car = services.car.create(db=db, obj_in=car_create_dto)
    return car


@router.put("/{id}", response_model=schemas.Car)
def update_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    car_update_dto: schemas.CarUpdateDto,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a car.
    """
    car = services.car.get(db=db, _id=id)

    if not car:
        raise CarNotFoundException()
    if not services.user.is_admin(current_user):
        raise NotEnoughPermissionsException()

    car = services.car.update(db=db, db_obj=car, obj_in=car_update_dto)
    return car
