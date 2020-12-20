from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import services
from app.core.config import settings
from app.schemas.user import UserCreateDto, UserUpdateDto
from app.tests.utils.utils import random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = services.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreateDto(username=email, email=email, password=password)
        services.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdateDto(password=password)
        services.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
