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
api = Api(blueprint, version='1.0', title='Developer API', description='Sample api to manage developers')
ns = api.namespace('v1', 'Operations on developer resources')
app.register_blueprint(blueprint)
log = logging.getLogger(__name__)


# ==== MODEL DEFINITIONS ==== 
developer_view = api.model('Developer', {
    'id': fields.Integer(),
    'name': fields.String(required=True, min_length=3, max_length=200),
    'team': fields.String(required=True, min_length=3, max_length=200),
    'skills': fields.List(fields.String),
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

# ===== PARSER ====
req_args = reqparse.RequestParser()
req_args.add_argument('name', type=str, required=False, help='Name of developer')
req_args.add_argument('team', type=str, required=False, help='Name of team')

# ===== SERVICE CLASS =====
class DeveloperService(object):
    def __init__(self):
        self.counter = 0
        self.developers = []

    def search(self, name, team): 
        return self.developers

    def get(self, id):
        for developer in self.developers:
            if developer['id'] == id:
                return developer
        api.abort(404, "Developer {} doesn't exist".format(id))

    def create(self, data):
        developer = data
        developer['id'] = self.counter = self.counter + 1
        developer['created_date'] = datetime.now()
        self.developers.append(developer)
        return developer

    def update(self, id, data):
        developer = self.get(id)
        developer.update(data)
        return developer

    def delete(self, id):
        developer = self.get(id)
        self.developers.remove(developer)

# init with some data
devServ = DeveloperService()
devServ.create({
    'name': 'Nam',
    'team': 'TheBugSpikers',
    'skills': ['test','dev','manage']
})
devServ.create({
    'name': 'Rahul',
    'team': 'TheBugSpikers',
    'skills': ['test', 'dev', 'manage']
})
devServ.create({
    'name': 'Sohrab',
    'team': 'TheBugSpikers',
    'skills': ['test', 'dev', 'manage']
})

# ==== FUNCTIONS ====
@ns.route('/health')
class HealthCheck(Resource):
    def get(self):
        return {
            'message': 'Server is healthy, checked at: ' + str(datetime.now())
        }

@ns.route('/developers/<int:id>')
@ns.response(404, 'Developer not found')
@api.doc(params={'id': 'Developer identifier'})
class UserSingle(Resource):
    @api.marshal_with(developer_view, code=200, description='Developer response')
    @api.response(200, 'Success')
    @api.doc('Get single developer')
    def get(self, id):
        log.info('Hello')
        return devServ.get(id)


@ns.route('/developers')
class DeveloperCollection(Resource):
    @api.marshal_with(developer_list_view)
    @api.response(200, 'Success')
    @api.doc('Get all developers')
    @api.expect(req_args)
    def get(self, **kwargs):
        args = req_args.parse_args(request)
        name = args.get('name')
        team = args.get('team')
        return {
            "items": devServ.search(team, name)
        }
        
    @api.marshal_with(developer_view)
    @api.response(201, 'Developer created')
    @api.expect(developer_view, validate=True)
    @api.doc('Create new developer')
    def post(self, **kwargs):
        return devServ.create(api.payload), 201

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
