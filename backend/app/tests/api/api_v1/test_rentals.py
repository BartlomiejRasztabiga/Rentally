from datetime import datetime, timedelta

import pytz
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.car import create_test_car
from app.tests.utils.customer import create_test_customer
from app.tests.utils.rental import create_test_rental
from app.tests.utils.reservation import create_test_reservation
from app.tests.utils.utils import get_datetime


def test_create_rental(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    data = {
        "car_id": car.id,
        "customer_id": customer.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "IN_PROGRESS",
    }
    response = client.post(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content


def test_create_rental_with_car_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    data = {
        "car_id": 9999999999,
        "customer_id": customer.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "IN_PROGRESS",
    }
    response = client.post(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 404


def test_create_rental_with_customer_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    data = {
        "car_id": car.id,
        "customer_id": 9999999999,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "IN_PROGRESS",
    }
    response = client.post(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 404


def test_create_rental_with_reservation(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    reservation = create_test_reservation(db, car, customer, start_date, end_date)

    data = {
        "car_id": car.id,
        "customer_id": customer.id,
        "reservation_id": reservation.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "IN_PROGRESS",
    }
    response = client.post(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content


def test_create_rental_with_reservation_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    data = {
        "car_id": car.id,
        "customer_id": customer.id,
        "reservation_id": 999999999999,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "IN_PROGRESS",
    }
    response = client.post(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 404


def test_get_rentals(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/rentals/", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_overtime_rentals(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = datetime.now(tz=pytz.UTC)
    end_date = datetime.now(tz=pytz.UTC) + timedelta(milliseconds=1)

    create_test_rental(db, car, customer, start_date, end_date)

    response = client.get(
        f"{settings.API_V1_STR}/rentals/overtime", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_rental_by_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    response = client.get(
        f"{settings.API_V1_STR}/rentals/{rental.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200


def test_get_rental_by_id_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/rentals/9999999999", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_delete_rental(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = get_datetime(2030, 12, 24)
    end_date = get_datetime(2030, 12, 25)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    response = client.delete(
        f"{settings.API_V1_STR}/rentals/{rental.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200


def test_delete_rental_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/rentals/99999999999", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_update_rental(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    car = create_test_car(db)
    customer = create_test_customer(db)

    start_date = datetime.now(tz=pytz.UTC)
    end_date = datetime.now(tz=pytz.UTC) + timedelta(milliseconds=1)

    rental = create_test_rental(db, car, customer, start_date, end_date)

    data = {
        "car_id": rental.car_id,
        "customer_id": rental.customer_id,
        "start_date": rental.start_date.isoformat(),
        "end_date": rental.end_date.isoformat(),
        "status": "COMPLETED",
    }

    response = client.put(
        f"{settings.API_V1_STR}/rentals/{rental.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200


def test_update_rental_not_existing(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "car_id": 1,
        "customer_id": 1,
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "status": "COMPLETED",
    }

    response = client.put(
        f"{settings.API_V1_STR}/rentals/999999999999",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
