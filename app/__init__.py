from flask import Flask, render_template
from flask_restful import Api

# views for frontend stuff
from app.views.index import index

# resources
# TODO: Rename resource files/classes
from app.resources.users import Users, UsersSingle
from app.resources.messages import Messages, MessageSingle, MessageSeen


def create_app():
    """
    Creates and configures flask api and app.
    Adds resources defined in app.resources.

    :return: preconfigured api
    """

    app = Flask(__name__)

    # Environment configuration
    app.config.from_object("config")

    # views rules
    app.add_url_rule(rule="/", endpoint="index", view_func=index)

    # Blueprints could be used?
    api = Api(app)

    # Add resources here
    api.add_resource(Users, "/users")

    api.add_resource(Messages, "/messages")
    api.add_resource(MessageSingle, "/messages/<string:message_id>")
    api.add_resource(MessageSeen, "/messages/<string:message_id>/<string:seen_id>")
    api.add_resource(UsersSingle, "/users/<string:user_id>")

    return app
