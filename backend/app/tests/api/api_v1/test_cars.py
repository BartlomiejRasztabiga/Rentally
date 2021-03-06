from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.car import create_test_car


def test_create_car(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "model_name": "Foo",
        "type": "CAR",
        "fuel_type": "DIESEL",
        "gearbox_type": "AUTO",
        "ac_type": "AUTO",
        "number_of_passengers": 4,
        "drive_type": "FRONT",
        "number_of_airbags": 8,
        "price_per_day": "99.99",
    }
    response = client.post(
        f"{settings.API_V1_STR}/cars/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["model_name"] == data["model_name"]
    assert content["type"] == data["type"]
    assert content["number_of_passengers"] == data["number_of_passengers"]
    assert "id" in content


def test_get_car_by_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    response = client.get(
        f"{settings.API_V1_STR}/cars/{car.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == car.id
    assert content["model_name"] == car.model_name
    assert content["type"] == "CAR"
    assert content["number_of_passengers"] == car.number_of_passengers


def test_get_car_by_id_not_exists(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/cars/999999999999", headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_update_car(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)

    data = {
        "model_name": "test",
        "type": "CAR",
        "fuel_type": "DIESEL",
        "gearbox_type": "AUTO",
        "ac_type": "AUTO",
        "number_of_passengers": 8,
        "drive_type": "FRONT",
        "number_of_airbags": 8,
        "price_per_day": "99.99",
    }
    response = client.put(
        f"{settings.API_V1_STR}/cars/{car.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == car.id
    assert content["model_name"] == car.model_name
    assert content["type"] == "CAR"
    assert content["number_of_passengers"] == data["number_of_passengers"]


def test_delete_car(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)

    response = client.delete(
        f"{settings.API_V1_STR}/cars/{car.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/cars/{car.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_delete_car_no_permissions(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)

    response = client.delete(
        f"{settings.API_V1_STR}/cars/{car.id}", headers=normal_user_token_headers,
    )
    assert response.status_code == 401
