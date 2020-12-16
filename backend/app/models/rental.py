import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# fmt: off
class RentalStatus(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


# fmt: on

# to properly initialise relationships

if TYPE_CHECKING:
    from .car import Car  # noqa: F401
    from .customer import Customer  # noqa: F401
    from .reservation import Reservation  # noqa: F401


class Rental(Base):
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    car = relationship("Car", back_populates="rentals", lazy=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="rentals", lazy=False)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), nullable=True)
    reservation = relationship("Reservation", back_populates="rental", lazy=False)
    start_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Enum(RentalStatus), nullable=False)
