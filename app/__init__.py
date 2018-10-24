from flask import Flask
from flask_restful import Api

# resources
# TODO: Rename resource files/classes
from app.resources.users import Users


def create_app():
    """
    :return: preconfigured api
    """

    app = Flask(__name__)

    # Environment configuration
    app.config.from_object("config")

    # Blueprints could be used?
    api = Api(app)

    # Add resources here
    api.add_resource(Users, "/users")

    return app
