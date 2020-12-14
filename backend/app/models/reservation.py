import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer

from app.db.base_class import Base


# fmt: off
class ReservationStatus(enum.Enum):
    NEW = "NEW"
    COLLECTED = "COLLECTED"
    CANCELLED = "CANCELLED"


# fmt: on


class Reservation(Base):
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False)
