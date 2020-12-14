from fastapi import HTTPException


class InstanceNotFoundException(HTTPException):
    def __init__(self, model_name):
        super().__init__(404, f"{model_name} not found")


class CarNotFoundException(InstanceNotFoundException):
    def __init__(self):
        super().__init__("Car")


class CustomerNotFoundException(InstanceNotFoundException):
    def __init__(self):
        super().__init__("Customer")
