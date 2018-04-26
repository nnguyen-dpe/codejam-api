# Rest view model for api requests and responses
from flask_restplus import fields
from apis.api import api
from apis.exceptions import ApiError

_developer = api.model('Developer', {
    'id': fields.String(required=False, readOnly=True),
    'name': fields.String(required=True, min_length=3, max_length=200),
    'team': fields.String(required=False),
    'skills': fields.List(fields.String)
})

_developer_list = api.model('DeveloperCollection', {
    'totalRecords': fields.Integer(required=True),
    'page': fields.Integer(required=True),
    'totalPages': fields.Integer(required=True),
    'records': fields.List(fields.Nested(_developer))
})

_err = api.model('Error', {
    'errorCode': fields.String(required=True, description='Error types',
                               enum=ApiError._member_names_),
    'errorDescription': fields.String(required=True)
})
