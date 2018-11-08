import logging
import threading, queue

from flask import Flask, render_template
from flask_restful import Api


# views for frontend stuff
from app.views.index import index

# resources
# TODO: Rename resource files/classes
from app.resources.users import Users, UsersSingle
from app.resources.messages import Messages, MessageSingle, MessageSeen

# channels
from app.channels.irc import IRC, run_irc
from app.database.db_handler import database_handler

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')  # TODO reformat
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def create_app(args):
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

    #if not args.disable_bots:
    Channels()
    logger.warning(database_handler().get_messages())

    logger.warning("Init channels is done")

    return app


class Channels:
    """
    Creates instances of channels
    """
    def __init__(self):
        # define server address
        # spawn threads
        self.queue = queue.Queue()
        threading.Thread(target=run_irc).start()
