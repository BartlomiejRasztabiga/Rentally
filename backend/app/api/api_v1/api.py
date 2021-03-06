from fastapi import APIRouter

from app.api.api_v1.endpoints import cars, customers, login, rentals, reservations, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(
    reservations.router, prefix="/reservations", tags=["reservations"]
)
api_router.include_router(rentals.router, prefix="/rentals", tags=["rentals"])
