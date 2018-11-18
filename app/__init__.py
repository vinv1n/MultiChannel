import logging
import threading, queue

from flask import Flask, render_template
from flask_restful import Api

from flask import request
from flask_restful import Resource
import json

# views for frontend stuff
from app.views.index import index
from app.database.db_handler import database_handler


db_handler = database_handler()
db_handler.__init__()

# resources
from app.resources.users import Users
from app.resources.users import UsersSingle
from app.resources.messages import Messages
from app.resources.messages import MessageSingle
from app.resources.messages import MessageSeen

# channels
#from app.channels.irc import IRC, run_irc
#from app.database.db_handler import database_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    api.add_resource(Users, "/users",
        resource_class_kwargs={ 'db_handler': db_handler })
    api.add_resource(Messages, '/messages',
        resource_class_kwargs={ 'db_handler': db_handler })
    api.add_resource(MessageSingle, "/messages/<string:message_id>",
        resource_class_kwargs={ 'db_handler': db_handler })
    api.add_resource(MessageSeen, "/messages/<string:message_id>/<string:seen_id>",
        resource_class_kwargs={ 'db_handler': db_handler })
    api.add_resource(UsersSingle, "/users/<string:user_id>",
        resource_class_kwargs={ 'db_handler': db_handler })

    #if not args.disable_bots:
    #Channels()
    #database_handler()

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


