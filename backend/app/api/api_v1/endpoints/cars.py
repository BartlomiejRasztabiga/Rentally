from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Car])
def get_cars(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cars.
    """
    cars = crud.car.get_multi(db, skip=skip, limit=limit)
    return cars


@router.post("/", response_model=schemas.Car)
def create_car(
        *,
        db: Session = Depends(deps.get_db),
        car_create_dto: schemas.CarCreateDto,
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new car.
    """
    if not crud.user.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    car = crud.car.create(db=db, obj_in=car_create_dto)
    return car
