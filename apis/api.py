from flask_restplus import Api
from apis.exceptions import NotFoundException, InvalidRequestException, ApiError

desc = """
As every good project manager knows, developers are interchangeable and they 
can be added to or removed from a project without any impacts. 
This API provides this functionality to the project managers.
"""

api = Api(
    version='1.0', 
    title='Developer API', 
    description=desc,
    tags='developer'
)

@api.errorhandler
def default_exception_handler(error):
    return {
        'errorCode': ApiError.InternalServerError.name,
        'errorDescription': error.message
    }, 500

@api.errorhandler(NotFoundException)
def notfound_exception_handler(error):
    return {
        'errorCode': ApiError.NotFound.name,
        'errorDescription': error.message
    }, 404

@api.errorhandler(InvalidRequestException)
def invalidrequest_exception_handler(error):
    return {
        'errorCode': ApiError.InvalidRequest.name,
        'errorDescription': error.message
    }, 400

