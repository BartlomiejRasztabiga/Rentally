from sqlalchemy.orm import Session

from app import crud
from app.schemas import CustomerUpdateDto
from app.tests.utils.customer import get_test_customer_create_dto


def test_create_customer(db: Session) -> None:
    customer_create_dto = get_test_customer_create_dto()
    customer = crud.customer.create(db=db, obj_in=customer_create_dto)

    assert customer.full_name == customer_create_dto.full_name
    assert customer.address == customer_create_dto.address
    assert customer.phone_number == customer_create_dto.phone_number
    assert customer.id is not None


def test_get_customer(db: Session) -> None:
    customer_create_dto = get_test_customer_create_dto()
    customer = crud.customer.create(db=db, obj_in=customer_create_dto)

    stored_customer = crud.customer.get(db=db, _id=customer.id)

    assert stored_customer
    assert stored_customer.full_name == customer_create_dto.full_name
    assert stored_customer.address == customer_create_dto.address
    assert stored_customer.phone_number == customer_create_dto.phone_number
    assert stored_customer.id is not None


def test_update_customer(db: Session) -> None:
    customer_create_dto = get_test_customer_create_dto()
    customer = crud.customer.create(db=db, obj_in=customer_create_dto)

    customer_update_dto = CustomerUpdateDto(full_name="Test customer 2")  # type: ignore
    updated_customer = crud.customer.update(db=db, db_obj=customer, obj_in=customer_update_dto)

    assert customer.id == updated_customer.id
    assert updated_customer.full_name is not None
    assert updated_customer.full_name == customer_update_dto.full_name


def test_delete_customer(db: Session) -> None:
    customer_create_dto = get_test_customer_create_dto()
    customer = crud.customer.create(db=db, obj_in=customer_create_dto)

    deleted_customer = crud.customer.remove(db=db, _id=customer.id)
    customer_after_delete = crud.customer.get(db=db, _id=customer.id)

    assert customer_after_delete is None
    assert deleted_customer.id == customer.id
    assert deleted_customer.full_name == customer_create_dto.full_name
    assert deleted_customer.address == customer_create_dto.address
    assert deleted_customer.phone_number == customer_create_dto.phone_number
