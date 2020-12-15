from fastapi import HTTPException


class StartDateNotBeforeEndDateException(HTTPException):
    def __init__(self):
        super().__init__(400, "Start date has to be before end date")


class ReservationCollisionException(HTTPException):
    def __init__(self):
        super().__init__(
            400, "There is already a reservation for this car in given time range"
        )


class UpdatingCancelledReservationException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot update cancelled reservation")


class InvalidStatusTransitionReservationException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot update this reservations's status")
