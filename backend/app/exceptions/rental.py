from fastapi import HTTPException


class RentalCollisionException(HTTPException):
    def __init__(self):
        super().__init__(
            400,
            "There is already a rental for this car in given time"
            " range or this car is unavailable",
        )


class UpdatingCompletedRentalException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot update completed rental")


class RentalCreatedInThePastException(HTTPException):
    def __init__(self):
        super().__init__(400, "Rental cannot be created in the past")


class RentalAndReservationDifferenceException(HTTPException):
    def __init__(self):
        super().__init__(
            400,
            "Rental's car_id or customer_id is different than on Reservation's object",
        )
