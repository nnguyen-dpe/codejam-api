# Define api routes for namespace
import logging

from flask import request
from flask_restplus import Resource, Namespace
from datetime import datetime
from apis.api import api
from apis.views import _developer, _developer_list, _err, ApiError
from apis.parsers import _get_devs_req, _post_dev_req
from apis.service import _srv
from apis.exceptions import NotFoundException, InvalidRequestException

ns = Namespace(
    name='developers', 
    description="Developer related operations"
)

log = logging.getLogger(__name__)


@ns.route('/health')
class HealthCheck(Resource):
    @api.response(200, 'Health check ok')
    def get(self):
        return {
            'message': 'Health checked at: ' + str(datetime.now())
        }, 200

@ns.route('/developers')
@api.response(400, 'Invalid request', _err)
@api.response(500, 'Internal server error', _err)
class DeveloperCollection(Resource):
    @api.marshal_with(_developer_list)
    @api.response(200, 
        'The search was performed successfully', _developer_list)
    @api.expect(_get_devs_req)
    @api.doc(description='Get developers', id='getDevelopers')
    def get(self, **kwargs):
        args = _get_devs_req.parse_args(request)
        return _srv.search(args), 200
    
    #@api.marshal_with(_developer, code=201, description='Developer created')
    @api.expect(_developer)
    @api.doc(description='Create a new developer', id='createDeveloper')
    def post(self, **kwargs):        
        try:
            _post_dev_req.parse_args(request)
            data = request.json
            return _srv.create(data), 201
        except:
            return {
                'errorCode': 'InvalidRequest',
                'errorDescription': 'Bad'
            }, 400


@ns.route('/developers/<string:id>', doc={'params': {'id': 'Developer id'}})
@api.response(404, 'Resource not found', _err)
@api.response(500, 'Internal server error', _err)
class DeveloperSingle(Resource):
    # @api.marshal_with(_developer, 
    #     code=200, description='The developer was successfully found')
    @api.doc(description='Get developer', id='getDeveloper')
    def get(self, id):
        obj = _srv.getOne(id)
        if obj:
            return obj, 200
        
        return {
            'errorCode': 'NotFound',
            'errorDescription': 'Developer not found for id: ' + id 
        }, 404



@ns.route('/developers/<string:id>/avatar', 
    doc={'params': {'id': 'Developer id'}})
@api.response(404, 'Resource not found', _err)
@api.response(500, 'Internal server error', _err)
class DeveloperAvatarSingle(Resource):
    @api.doc(description='Get developer avatar', id='getDeveloperAvatar')
    def get(self, id):
        obj = _srv.getOne(id)
        if obj:
            return obj, 200

        return {
            'errorCode': 'NotFound',
            'errorDescription': 'Developer not found for id: ' + id
        }, 404


@ns.route('/avatars/upload')
@api.response(500, 'Internal server error', _err)
class AvatarUpload(Resource):
    @api.doc(description='Upload avatar', id='uploadAvatar')
    def post(self):
        return {}, 200