from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.schemas.customer import CustomerCreateDto, CustomerUpdateDto


class CRUDCustomer(CRUDBase[Customer, CustomerCreateDto, CustomerUpdateDto]):
    pass


customer = CRUDCustomer(Customer)
