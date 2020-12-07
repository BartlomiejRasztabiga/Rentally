from app.crud.base import CRUDBase
from app.models import Truck


class CRUDTruck(CRUDBase[Truck]):
    pass


#     def get_all(self, db: Session, *) -> Optional[User]:
#         return db.query(User).filter(User.email == email).first()
#
#     def create(self, db: Session, *, obj_in: UserCreateDto) -> User:
#         db_obj = User(
#             email=obj_in.email,
#             hashed_password=get_password_hash(obj_in.password),
#             full_name=obj_in.full_name,
#             is_admin=obj_in.is_admin,
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj


truck = CRUDTruck(Truck)
