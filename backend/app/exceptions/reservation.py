from fastapi import HTTPException


class StartDateNotBeforeEndDateException(HTTPException):
    def __init__(self):
        super().__init__(400, "Start date has to be before end date")


class ReservationCreatedInThePastException(HTTPException):
    def __init__(self):
        super().__init__(400, "Reservation cannot be created in the past")


class ReservationCollisionException(HTTPException):
    def __init__(self):
        super().__init__(
            400,
            "There is already a reservation for this car in given time"
            " range or this car is unavailable",
        )


class UpdatingCancelledReservationException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot update cancelled reservation")


class UpdatingCollectedReservationException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot update collected reservation")


class CancelReservationWithRentalException(HTTPException):
    def __init__(self):
        super().__init__(400, "You cannot cancel a reservation that has related rental")
