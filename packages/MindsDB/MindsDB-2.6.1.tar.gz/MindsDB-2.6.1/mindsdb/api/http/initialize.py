from flask import Flask, url_for
from flask_restx import Api
from flask_cors import CORS
import json

from mindsdb.interfaces.datastore.datastore import DataStore
from mindsdb.interfaces.native.mindsdb import MindsdbNative
from mindsdb.utilities.config import Config


class Swagger_Api(Api):
    """
    This is a modification of the base Flask Restplus Api class due to the issue described here
    https://github.com/noirbizarre/flask-restplus/issues/223
    """
    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"), _external=False)

def initialize_flask(config):
    app = Flask(__name__, static_url_path='/static')

    app.config['SWAGGER_HOST'] = 'http://localhost:8000/mindsdb'
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'query',
            'name': 'apikey'
        }
    }
    cors_origin_list = ["http://localhost:5000", "http://localhost:3000"]
    cors = CORS(app, resources={r"/*": {"origins": cors_origin_list}})

    api = Swagger_Api(app, authorizations=authorizations, security=['apikey'], url_prefix=':8000')

    return app, api

def initialize_interfaces(config, app):
    app.default_store = DataStore(config)
    app.mindsdb_native = MindsdbNative(config)
    app.config_obj = config
