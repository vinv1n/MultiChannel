import logging
import threading
import time

from flask import Flask, render_template
from flask_restful import Api

from queue import Queue

# views for frontend stuff
from app.views.index import index

# resources
# TODO: Rename resource files/classes
from app.resources.users import Users, UsersSingle
from app.resources.messages import Messages, MessageSingle, MessageSeen

# channels
from app.channels.irc import run_irc
from app.database.db_handler import database_handler

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s:%(name)-s:%(levelname)s %(message)s",
                        datefmt="%a, %d %b %Y %H:%M:%S", filemode="w", filename="/tmp/multi.log")


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)-15s:%(name)-s:%(levelname)s %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")  # TODO reformat
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

    # Add resources here
    api.add_resource(Users, "/users")

    api.add_resource(Messages, "/messages")
    api.add_resource(MessageSingle, "/messages/<string:message_id>")
    api.add_resource(MessageSeen, "/messages/<string:message_id>/<string:seen_id>")
    api.add_resource(UsersSingle, "/users/<string:user_id>")

    #if not args.disable_bots:
    Channels().create_irc_thread()

    logger.info("Init channels is done")

    return app


class Channels:
    """
    Creates instances of channels
    """
    def __init__(self):
        self.queue_in_irc = Queue()
        self.queue_out_irc = Queue()

    def create_irc_thread(self):
        # FIXME this is horrible solution
        threading.Thread(target=run_irc(queue_in=self.queue_in_irc, queue_out=self.queue_out_irc)).start()
        self.queue_in_irc.put("iamhere")
        logger.info(self.queue_in_irc)
