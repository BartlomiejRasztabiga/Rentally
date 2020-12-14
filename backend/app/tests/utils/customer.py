from sqlalchemy.orm import Session

from app import models, crud
from app.schemas.customer import CustomerCreateDto


def get_test_customer_create_dto() -> CustomerCreateDto:
    customer_create_dto = CustomerCreateDto(
        full_name="Test customer",
        address="ul. Krzewiasta 119, 70-732 Szczecin",
        phone_number="51 404 37695",
    )
    return customer_create_dto


def create_random_customer(db: Session) -> models.Customer:
    customer_create_dto = get_test_customer_create_dto()
    return crud.customer.create(db=db, obj_in=customer_create_dto)
