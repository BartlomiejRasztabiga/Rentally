from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# to properly initialise relationships

if TYPE_CHECKING:
    from .reservation import Reservation  # noqa: F401
    from .rental import Rental  # noqa: F401


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    reservations = relationship("Reservation")
    rentals = relationship("Rental")
