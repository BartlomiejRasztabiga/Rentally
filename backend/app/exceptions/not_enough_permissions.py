from fastapi import HTTPException


class NotEnoughPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(401, "Not enough permissions")
