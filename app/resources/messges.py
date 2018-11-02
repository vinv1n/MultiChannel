"""
Messages resource class.
"""

from flask import request
from flask_restful import Resource


class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """

    @staticmethod
    def get():
        """
        Get a list of all messages in database.
        """
        messages = list()

        return {'messages': messages}

    @staticmethod
    def post():
        """
        Send a new message.
        """
        message = request.form['message']

        return {}, 201


class MessageSinge(Resource):
    """
    For handling single messages in database.
    """

    @staticmethod
    def get(message_id):
        """
        Return all information of a single message.
        """
        message = None
        return {'message': message}

    @staticmethod
    def delete(message_id):
        """
        Delete a message with the given ID.
        """

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
