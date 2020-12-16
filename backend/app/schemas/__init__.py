from .car import Car, CarCreateDto, CarInDB, CarUpdateDto
from .customer import Customer, CustomerCreateDto, CustomerInDB, CustomerUpdateDto
from .token import Token, TokenPayload
from .user import User, UserCreateDto, UserInDB, UserUpdateDto

from .reservation import (  # isort:skip
    Reservation,
    ReservationCreateDto,
    ReservationInDB,
    ReservationUpdateDto,
)
from .rental import Rental, RentalCreateDto, RentalInDB, RentalUpdateDto  # isort:skip
