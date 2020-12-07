from sqlalchemy import Column, Float, ForeignKey, Integer

from app.db.base_class import Base


class Truck(Base):
    id = Column(Integer, ForeignKey("car.id"), primary_key=True, index=True)
    loading_capacity = Column(Float, nullable=True, index=True)
    boot_width = Column(Float, nullable=True)
    boot_height = Column(Float, nullable=True)
    boot_length = Column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "truck",
    }
