from fastapi import HTTPException


class StartDateNotBeforeEndDateException(HTTPException):
    def __init__(self):
        super().__init__(400, "Start date has to be before end date")


class ReservationCollisionException(HTTPException):
    def __init__(self):
        super().__init__(400, "There is already a reservation for this car in given time range")
