from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.exceptions.instance_not_found import CustomerNotFoundException

router = APIRouter()


@router.get("/", response_model=List[schemas.Customer])
def get_customers(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve customers.
    """
    customers = crud.customer.get_all(db)
    return customers


@router.get("/{id}", response_model=schemas.Customer)
def get_customer(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get customer by ID.
    """
    customer = crud.customer.get(db=db, _id=id)
    if not customer:
        raise CustomerNotFoundException()

    return customer


@router.delete("/{id}", response_model=schemas.Customer)
def delete_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a customer.
    """
    customer = crud.customer.get(db=db, _id=id)

    # TODO check if has relations to rentals/reservations

    if not customer:
        raise CustomerNotFoundException()

    customer = crud.customer.remove(db=db, _id=id)
    return customer


@router.post("/", response_model=schemas.Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_create_dto: schemas.CustomerCreateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new customer.
    """

    customer = crud.customer.create(db=db, obj_in=customer_create_dto)
    return customer


@router.put("/{id}", response_model=schemas.Customer)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    customer_update_dto: schemas.CustomerUpdateDto,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a customer.
    """
    customer = crud.customer.get(db=db, _id=id)

    if not customer:
        raise CustomerNotFoundException()

    customer = crud.customer.update(db=db, db_obj=customer, obj_in=customer_update_dto)
    return customer
