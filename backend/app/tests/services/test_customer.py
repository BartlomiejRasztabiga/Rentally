from sqlalchemy.orm import Session

from app import services
from app.schemas import CustomerUpdateDto
from app.tests.utils.customer import create_test_customer, get_test_customer_create_dto


def test_create_customer(db: Session) -> None:
    customer_create_dto = get_test_customer_create_dto()
    customer = services.customer.create(db=db, obj_in=customer_create_dto)

    assert customer.full_name == customer_create_dto.full_name
    assert customer.address == customer_create_dto.address
    assert customer.phone_number == customer_create_dto.phone_number
    assert customer.id is not None


def test_get_customer(db: Session) -> None:
    customer = create_test_customer(db)

    stored_customer = services.customer.get(db=db, _id=customer.id)

    assert stored_customer
    assert stored_customer.full_name == customer.full_name
    assert stored_customer.address == customer.address
    assert stored_customer.phone_number == customer.phone_number
    assert stored_customer.id is not None


def test_update_customer(db: Session) -> None:
    customer = create_test_customer(db)

    customer_update_dto = CustomerUpdateDto(full_name="Test customer 2")  # type: ignore
    updated_customer = services.customer.update(
        db=db, db_obj=customer, obj_in=customer_update_dto
    )

    assert customer.id == updated_customer.id
    assert updated_customer.full_name is not None
    assert updated_customer.full_name == customer_update_dto.full_name


def test_delete_customer(db: Session) -> None:
    customer = create_test_customer(db)

    deleted_customer = services.customer.remove(db=db, _id=customer.id)
    customer_after_delete = services.customer.get(db=db, _id=customer.id)

    assert customer_after_delete is None
    assert deleted_customer.id == customer.id
    assert deleted_customer.full_name == customer.full_name
    assert deleted_customer.address == customer.address
    assert deleted_customer.phone_number == customer.phone_number
