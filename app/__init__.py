from flask import Flask

from .api.v1.views.parcels import parcels_api
from .api.v1.views.users import users_api

def create_app(configuration):
    """Creates the flask app"""

    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(parcels_api, url_prefix='/api/v1')
    app.register_blueprint(users_api, url_prefix='/api/v1')

    return app
