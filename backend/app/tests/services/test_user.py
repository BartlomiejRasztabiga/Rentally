from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import services
from app.core.security import verify_password
from app.schemas.user import UserCreateDto, UserUpdateDto
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateDto(email=email, password=password)
    user = services.user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateDto(email=email, password=password)
    user = services.user.create(db, obj_in=user_in)
    authenticated_user = services.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = services.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_admin(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateDto(email=email, password=password, is_admin=True)
    user = services.user.create(db, obj_in=user_in)
    is_admin = services.user.is_admin(user)
    assert is_admin is True


def test_check_if_user_is_admin_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreateDto(email=username, password=password)
    user = services.user.create(db, obj_in=user_in)
    is_admin = services.user.is_admin(user)
    assert is_admin is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreateDto(email=username, password=password, is_admin=True)
    user = services.user.create(db, obj_in=user_in)
    user_2 = services.user.get(db, _id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreateDto(email=email, password=password, is_admin=True)
    user = services.user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdateDto(password=new_password, is_admin=True)
    services.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = services.user.get(db, _id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
