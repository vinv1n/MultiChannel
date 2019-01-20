import logging
import threading
import time
import queue
import os
import json

from flask import Flask, render_template, redirect, request
from flask_restful import Api, reqparse
from flask_json_schema import JsonSchema, JsonValidationError
from flask_sslify import SSLify
from utils import MultiChannelException

from queue import Queue
from app.resources.users import Users, UserSingle
from app.resources.messages import Messages, MessageSingle, MessageSeen
from app.resources.updates import Update
from app.resources.authentication import UserLogin, Logout, RefreshLogin, RefreshLogout

from app.error_handlers import json_validation_error

# views for frontend stuff
from app.views.index import index
from app.views.webpage import webpage

from app.database.db_handler import database_handler
from app.resources.message_handler import Message_handler

from functools import partial
from flask_jwt_extended import JWTManager

from app.channels.email_handler import EmailHandler
from app.channels.telegram_bot import Telegram
from app.channels.irc_handler import IRC



def _channel(body, _type, group, user, channel_info, _name):
    """
    Dummy channel, these are the inputs (except _name) of channels.

    IRC()
    Telegram()
    EmailHandler()
    """

def _init_channels():
    def load_config():
        conf = None
        try:
            with open("./config.json", "r") as config:
                conf = json.loads(config.read())
        except (IOError, OSError, KeyError):
            return None
        if not conf:
            return {}

        return conf["channels"]

    def get_channel_config(conf):
        email = config["email"]
        telegram = config["telegram"]
        irc = config["irc"]
        return irc, telegram, email

    config = load_config()
    if not config:
        raise MultiChannelException("Could not import channels configutations")

    irc, telegram, email = get_channel_config(conf=config)

    _channels = {
        "irc": IRC().send_message,
        "telegram": Telegram(telegram.get("token")),
        "email": EmailHandler(password=email.get("password"), address=email.get("address"),
                                imap_server=email.get("imap"), host=email.get("smtp"))
    }
    
    return _channels

# for log file
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
    app = Flask(__name__, instance_relative_config=True)

    # register json validation schema
    # NOTE: needs to be passed to different views and register specific schema
    schema = JsonSchema(app)

    # Environment configuration from instance directory
    app.config.from_pyfile("config.py")

    sslify = SSLify(app)

    # views rules
    app.add_url_rule(rule="/", endpoint="index", view_func=index)

    # custom error handler for json validation errors
    app.register_error_handler(JsonValidationError, json_validation_error)

    # Add webpage to app
    app = webpage(app)

    api = Api(app)

    channels = _init_channels()
    db_handler = database_handler()
    message_handler = Message_handler(channels=channels, _database_handler=db_handler)

    jwt = JWTManager(app)
    blacklist = set()


    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(token):
        jti = token['jti']
        return jti in blacklist

    api.add_resource(
        UserLogin,
        "/api/user-login",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt}
    )
    api.add_resource(
        RefreshLogin,
        "/api/re-login", #Maybe change this to something that might be more suitable? Patch request to login?
        resource_class_kwargs={'db_handler': db_handler, 'jwt':jwt},
    )
    api.add_resource(
        Logout,
        "/api/logout",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt, 'blacklist':blacklist},
    )
    api.add_resource(
        RefreshLogout,
        "/api/re-logout",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt, 'blacklist':blacklist},
    )
    api.add_resource(
        Users,
        "/api/users",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt},
    )
    api.add_resource(
        UserSingle,
        "/api/users/<string:user_id>",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt}
    )
    api.add_resource(
        Messages,
        "/api/messages",
        resource_class_kwargs={'db_handler': db_handler, 'message_handler': message_handler,'jwt':jwt},
    )
    api.add_resource(
        MessageSingle,
        "/api/messages/<string:message_id>",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt},
    )
    api.add_resource(
        MessageSeen,
        "/api/messages/<string:message_id>/<string:seen_id>",
        resource_class_kwargs={'db_handler': db_handler,'jwt':jwt},
    )
    # enpoint to update messages to database
    api.add_resource(
        Update,
        "/api/channels/update",
        resource_class_kwargs={'db_handler': db_handler, "channels": channels},
    )

    logger.info("Init channels is done")

    return app
