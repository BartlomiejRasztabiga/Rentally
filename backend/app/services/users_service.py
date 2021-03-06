from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreateDto, UserUpdateDto
from app.services.base import BaseService


class UserService(BaseService[User, UserCreateDto, UserUpdateDto]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Returns user by email
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreateDto) -> User:
        """
        Creates new user
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateDto) -> User:
        """
        Updates given user
        """
        update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            obj_in.hashed_password = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Returns user if user exists and password is correct, returns None otherwise
        """
        _user = self.get_by_email(db, email=email)
        if not _user:
            return None
        if not verify_password(password, _user.hashed_password):
            return None
        return _user

    def is_admin(self, _user: User) -> bool:
        """
        Returns True if user is an admin, False otherwise
        """
        return _user.is_admin


user = UserService(User)
