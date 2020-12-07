from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.car import CarType

router = APIRouter()


@router.get("/", response_model=List[Union[schemas.Car, schemas.Truck]])
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


@router.post("/", response_model=Union[schemas.Car, schemas.Truck])
def create_car(
        *,
        db: Session = Depends(deps.get_db),
        car_create_dto: Union[schemas.TruckCreateDto, schemas.CarCreateDto],
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new car.
    """
    if not crud.user.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if car_create_dto.type == CarType.CAR:
        delattr(car_create_dto, 'type')
        car = crud.car.create(db=db, obj_in=car_create_dto)
    elif car_create_dto.type == CarType.TRUCK:
        print(car_create_dto)
        delattr(car_create_dto, 'type')
        car = crud.truck.create(db=db, obj_in=car_create_dto)

    # TODO
    # decide by type, which crud to call (car, truck or sportscar)
    # car = crud.car.create(db=db, obj_in=car_create_dto)

    return car
