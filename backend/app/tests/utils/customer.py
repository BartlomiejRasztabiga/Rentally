from app.schemas.customer import CustomerCreateDto


def get_test_customer_create_dto() -> CustomerCreateDto:
    customer_create_dto = CustomerCreateDto(
        full_name="Test customer",
        address="ul. Krzewiasta 119, 70-732 Szczecin",
        phone_number="51 404 37695",
    )
    return customer_create_dto
