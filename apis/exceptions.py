from enum import Enum

class InvalidRequestException(Exception):
    status_code = 400

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

class NotFoundException(Exception):
    status_code = 404

    def __init__(self, message, status_code=404, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

class ApiError(Enum):
    NotFound = 404
    BadRequest = 400
    InternalServerError = 500
