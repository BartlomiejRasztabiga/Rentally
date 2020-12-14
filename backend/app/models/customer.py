from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
