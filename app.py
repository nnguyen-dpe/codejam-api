# app.py
import os
import logging

import boto3

from flask import Flask, jsonify, request, Blueprint
from flask_restplus import Resource, Api, fields, reqparse
from datetime import datetime

# ==== INIT ====
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, version='1.0', title='User API', description='Sample api to manage users')
ns = api.namespace('v1', 'Operations on user resources')
app.register_blueprint(blueprint)
log = logging.getLogger(__name__)


# ==== MODEL DEFINITIONS ==== 
developer_view = api.model('Developer', {
    'id': fields.Integer(required=True, min=0),
    'name': fields.String(required=True, min_length=3, max_length=200),
    'team': fields.String(required=True, min_length=3, max_length=200),
    'skills': fields.List(required=True),
    'created_date': fields.DateTime(dt_format='iso8601'),
})

developer_list_view = api.model('DeveloperCollection', {
    'items': fields.List(fields.Nested(developer_view))
})

class Developer(object):
    def __init__(self, id, name, team, skills):
        self.id = id
        self.name = name
        self.team = team
        self.skills = skills
        self.created_date = datetime.now()

# ===== SERVICE CLASS =====
class DeveloperService(object):
    def __init__(self):
        self.counter = 0
        self.developers = []

    def get(self, id):
        for developer in self.developers:
            if developer['id'] == id:
                return developer
        api.abort(404, "Developer {} doesn't exist".format(id))

    def create(self, data):
        developer = data
        developer['id'] = self.counter = self.counter + 1
        self.developers.append(developer)
        return developer

    def update(self, id, data):
        developer = self.get(id)
        developer.update(data)
        return developer

    def delete(self, id):
        developer = self.get(id)
        self.developers.remove(developer)


# ==== FUNCTIONS ====
@ns.route('/health')
class HealthCheck(Resource):
    def get(self):
        return {
            'message': 'Server is healthy'
        }

@ns.route('/users/<string:user_id>')
@api.doc(params={'user_id': 'User identifier'})
class UserSingle(Resource):
    @api.marshal_with(user_view, code=200, description='User response')
    @api.response(200, 'Success')
    @api.doc('Get single user')
    def get(self, **kwargs):
        log.info('Hello')
        return Developer(1, 'Demo')
    
    @api.expect(user_view, validate=True)
    @api.response(202, 'User updated')
    @api.doc('Update existing user')
    def put(self, **kwargs):
        return request.json


@ns.route('/users')
class UserCollection(Resource):
    @api.marshal_with(user_list_view)
    @api.response(200, 'Success')
    @api.doc('Get all users')
    def get(self, **kwargs):
        list = []
        for x in range(10):
            list.append(User(x, 'Test' + str(x)))
        return {
            'items': list
        }

    @api.response(201, 'User created')
    @api.expect(user_view, validate=True)
    @api.doc('Create new user')
    def post(self, **kwargs):
        user_id = request.json.get('user_id')
        name = request.json.get('name')
        return jsonify({
            'user_id': user_id,
            'name': name
        })

# def get_user(user_id):
#     resp = client.get_item(
#         TableName=USERS_TABLE,
#         Key={
#             'user_id': { 'S': user_id }
#         }
#     )
#     item = resp.get('Item')
#     if not item:
#         return jsonify({'error': 'User does not exist'}), 404
#     return jsonify(
#         {
#             'user_id': item.get('user_id').get('S'),
#             'name': item.get('name').get('S')
#         }
#     )


if __name__ == '__main__':
    app.run(debug=False)
