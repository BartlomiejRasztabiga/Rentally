from sqlalchemy import Column, Float, ForeignKey, Integer

from app.db.base_class import Base


class SportsCar(Base):
    id = Column(Integer, ForeignKey("car.id"), primary_key=True, index=True)
    horsepower = Column(Integer, nullable=True, index=True)
    zero_to_hundred_time = Column(Float, nullable=True)
    engine_capacity = Column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "sportscar",
    }
