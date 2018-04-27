import os

from flask import Flask
from apis.api import api
from apis.routes import ns as developer_ns

IS_OFFLINE = os.environ.get('IS_OFFLINE')
DEBUG = False
if IS_OFFLINE:
    DEBUG = True

app = Flask(__name__)
api.add_namespace(developer_ns, '/api/v1')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=DEBUG)
