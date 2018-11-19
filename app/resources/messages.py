from flask import request
from flask_restful import Resource


class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """

    def __init__(self, db_handler, message_handler):
        self.db_handler = db_handler
        self.message_handler = message_handler

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

        message = {}
        users = {}
        try:
            data = request.get_json()
            message = data['message']
            users = data['users']
        except Exception as e:
            return {'error': 'Sent data was in wrong form'}, 400

        try:
            message_id = self.message_handler.send_message(
                message=message,
                users=users,
            )
        except Exception as e:
            return {'error': e}, 400

        if message_id is not None:
            return {'message_id': message_id}
        else:
            return {'error': 'Could not sent the message'}, 400


class MessageSingle(Resource):
    """
    For handling single messages in database.
    """

    def __init__(self, db_handler):
        self.db_handler = db_handler

    def get(self, message_id):
        """
        Return all information of a single message.
        """
        message = self.db_handler.get_message(message_id)
        if message != {} or message is None:
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

    def __init__(self, db_handler):
        self.db_handler = db_handler

    def get(self, message_id, seen_id):
        """
        When this get message is processed,
        mark the message_id read by user_id.
        """
        # TODO: magic pixel handling
        return {}
