import logging
import threading
import time
import queue

from flask import Flask, render_template
from flask_restful import Api

from queue import Queue
from app.resources.users import Users, UserSingle
from app.resources.messages import Messages, MessageSingle, MessageSeen

# views for frontend stuff
from app.views.index import index
from app.database.db_handler import database_handler
from app.resources.message_handler import Message_handler

from functools import partial


def _channel(body, _type, group, user, channel_info, _name):
    """
    Dummy channel, these are the inputs (except _name) of channels.
    """
    logger.warning('This is channel {}'.format(_name))
    logger.warning('body: {}'.format(body))
    logger.warning('type: {}'.format(_type))
    logger.warning('group_message: {}'.format(group))
    logger.warning('user: {}'.format(user))
    logger.warning('Channel information: {}'.format(channel_info))


# channels
channels = {
    'email': partial(_channel, _name='email'),
    'slack': partial(_channel, _name='slack'),
}


from app.channels.irc import run_irc

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s:%(name)-s:%(levelname)s %(message)s",
                        datefmt="%a, %d %b %Y %H:%M:%S", filemode="w", filename="/tmp/multi.log")


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)-15s:%(name)-s:%(levelname)s %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)


def create_app(args):
    """
    Creates and configures flask api and app.
    Adds resources defined in app.resources.

    :return: preconfigured api
    """
    logger.debug("Creating Api")
    app = Flask(__name__)

    # Environment configuration
    app.config.from_object("config")

    # views rules
    app.add_url_rule(rule="/", endpoint="index", view_func=index)

    # Blueprints could be used?
    api = Api(app)

    db_handler = database_handler()
    message_handler = Message_handler(channels=channels, _database_handler=db_handler)

    # Resources
    api.add_resource(
        Users,
        "/users",
        resource_class_kwargs={'db_handler': db_handler},
    )
    api.add_resource(
        UserSingle,
        "/users/<string:user_id>",
        resource_class_kwargs={'db_handler': db_handler}
    )

    api.add_resource(
        Messages,
        "/messages",
        resource_class_kwargs={'db_handler': db_handler, 'message_handler': message_handler},
    )
    api.add_resource(
        MessageSingle,
        "/messages/<string:message_id>",
        resource_class_kwargs={'db_handler': db_handler},
    )
    api.add_resource(
        MessageSeen,
        "/messages/<string:message_id>/<string:seen_id>",
        resource_class_kwargs={'db_handler': db_handler},
    )

    logger.info("Init channels is done")

    return app