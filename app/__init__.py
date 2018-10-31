from flask import Flask
from flask_restful import Api

# resources
# TODO: Rename resource files/classes
from app.resources.users import Users
from app.resources.messages import Messages, MessageSingle, MessageSeen

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
    api.add_resource(Messages, "/messages")
    api.add_resource(MessageSingle, "/messages/<string:message_id>")
    api.add_resource(MessageSeen, "/messages/<string:message_id>/<string:seen_id>")

    return app
