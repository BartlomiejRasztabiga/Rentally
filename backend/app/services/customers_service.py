from app.models.customer import Customer
from app.schemas.customer import CustomerCreateDto, CustomerUpdateDto
from app.services.base import BaseService


class CustomerService(BaseService[Customer, CustomerCreateDto, CustomerUpdateDto]):
    pass


customer = CustomerService(Customer)
