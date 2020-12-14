from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.customer import create_random_customer


def test_create_customer(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "full_name": "Foo",
        "address": "Bar",
        "phone_number": "123",
    }
    response = client.post(
        f"{settings.API_V1_STR}/customers/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["full_name"] == data["full_name"]
    assert content["address"] == data["address"]
    assert content["phone_number"] == data["phone_number"]
    assert "id" in content


def test_get_customer_by_id(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    customer = create_random_customer(db)
    response = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == customer.id
    assert content["full_name"] == customer.full_name
    assert content["address"] == customer.address
    assert content["phone_number"] == customer.phone_number


def test_update_customer(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    customer = create_random_customer(db)

    data = {
        "phone_number": "123456789",
    }
    response = client.put(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == customer.id
    assert content["full_name"] == customer.full_name
    assert content["address"] == customer.address
    assert content["phone_number"] == data["phone_number"]


def test_delete_customer(
        client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    customer = create_random_customer(db)

    response = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 404
