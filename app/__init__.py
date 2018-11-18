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
database_handler.__init__

# resources
class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """

    @staticmethod
    def get():
        """
        Get a list of all messages in database.
        """
        messages = db_handler.get_messages()
        return {'messages': messages}

    @staticmethod
    def post():
        """
        Send a new message.
        """

        """ Create the message structure before passing it to the db_handler. Example
         message = {
            "_id": id, (This is created by MongoDB no need to specify manually)
            "content": str,
            "sender": str,
            "sent_to": {      
                user_id: {
                    "seen": bool,
                    "answer": str
                }
            }
        }"""

        message_data = {}
        sent_to = {}
        try:
            data = request.get_json()
            message_data.update({"content": data.get("content")})
            message_data.update({"sender": data.get("sender")})
            for user_id in data.get("sent_to"):
                sent_to[user_id] = {"seen" : False, "answer" : ""}
            message_data.update({"sent_to": sent_to})
        except Exception as e:
            return {}, 400


        response = db_handler.create_message(message_data)
        return {'message_id' : response}


class MessageSingle(Resource):
    """
    For handling single messages in database.
    """

    @staticmethod
    def get(message_id):
        """
        Return all information of a single message.
        """
        message = db_handler.get_message(message_id)
        if message != {} or message == None:
            return {'message': message}, 200
        else:
            return {"message": "No messages with id:"+message_id}, 404


    @staticmethod
    def delete(message_id):
        """
        Delete a message with the given ID.
        """
        response = db_handler.delete_message(message_id)
        return {}


class MessageSeen(Resource):
    """
    Handles marking messages seen by certain users.
    """

    @staticmethod
    def get(message_id, seen_id):
        """
        When this get message is processed,
        mark the message_id read by user_id.
        """
        # TODO: magic pixel handling
        return {}

class Users(Resource):
    """
    Resource to get and add users.
    """

    @staticmethod
    def get():
        response = db_handler.get_users()
        return {"Users" : response}

    @staticmethod
    def post():
        """ Post a new user to the database. Make a dictionary to pass to the db_handler.

        {
        username: string,
        uuid: string,  
        password: string,
        preferred_channel: string,
        channels: {
            {
            email: {address: string},
            facebook: {user_id: string},
            telegram: {user_id: string},
            irc: {
                nickname: string,
                network: string
                }
            slack: {
                channel: string,
                username: string
            }"""


        user_data = {}
        try:
            data = request.get_json()

            user_data["username"] = data.get("username")
            user_data["password"] = data.get("password")
            user_data["preferred_channel"] = data.get("preferred_channel")
            user_data["channels"] = data.get("channels")
        except Exception as e:
            return {}, 400

        response = db_handler.create_user(user_data)
        return {"user_id": response}


class UsersSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """

    @staticmethod
    def get(user_id):
        response =  db_handler.get_user(user_id)
        return {"User" : response }

    @staticmethod
    def patch(user_id):
        data = request.get_json()
        user_data = {}
        for key in data:
            user_data[str(key)] = data.get(key)
        response = db_handler.update_user(user_data, user_id)
        return {}, response


    @staticmethod
    def delete(user_id):
        response =  db_handler.delete_user(user_id)
        return {"Users" : response }
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
    api.add_resource(Users, "/users")

    api.add_resource(Messages, "/messages")
    api.add_resource(MessageSingle, "/messages/<string:message_id>")
    api.add_resource(MessageSeen, "/messages/<string:message_id>/<string:seen_id>")
    api.add_resource(UsersSingle, "/users/<string:user_id>")

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


