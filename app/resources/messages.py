from flask import request
from flask_restful import Resource
import json


class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """
    def __init__(self,**kwargs):
        self.db_handler = kwargs['db_handler']


    def get(self):
        """
        Get a list of all messages in database.
        """
        messages = self.db_handler.get_messages()
        return {'messages': messages}


    def post(self):
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


        response = self.db_handler.create_message(message_data)
        return {'message_id' : response}


class MessageSingle(Resource):
    """
    For handling single messages in database.
    """
    def __init__(self, **kwargs):
        self.db_handler = kwargs['db_handler']


    def get(self, message_id):
        """
        Return all information of a single message.
        """
        message = self.db_handler.get_message(message_id)
        if message != {} or message == None:
            return {'message': message}, 200
        else:
            return {"message": "No messages with id:"+message_id}, 404



    def delete(self, message_id):
        """
        Delete a message with the given ID.
        """
        response = self.db_handler.delete_message(message_id)
        return {}


class MessageSeen(Resource):
    """
    Handles marking messages seen by certain users.
    """
    def __init__(self, **kwargs):
        self.db_handler = kwargs['db_handler']


    def get(self, message_id, seen_id):
        """
        When this get message is processed,
        mark the message_id read by user_id.
        """
        # TODO: magic pixel handling
        return {}

