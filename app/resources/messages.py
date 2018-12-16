from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """

    def __init__(self, db_handler, message_handler, jwt):
        self.db_handler = db_handler
        self.message_handler = message_handler
        self.jwt = jwt

    @jwt_required
    def get(self):
        """
        Get a list of all messages in database.
        """
        response = self.db_handler.get_messages()
        if response == None:
            return {"Error": "Error during data handling"}
        else:
            return {'Messages': response}

    @jwt_required
    def post(self):
        """
        Send a new message.
        """
        try:
            args = {}
            data = request.get_json()
            args['message'] = data['message']
            args['sent_to'] = data['sent_to']
        except Exception as e:
            return {'Error' : "Malformed request. Include 'message' and 'sent_to' as a list of users"}, 400
        message_id = self.message_handler.send_message(
             message = args["message"],
                #sender = get_jwt_identity(),
            users = args["sent_to"]
        )
        if message_id is not None:
            return {'message_id': message_id}
        else:
            return {'Error': 'Could not post the message'}, 400


class MessageSingle(Resource):
    """
    For handling single messages in database.
    """

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt

    @jwt_required
    def get(self, message_id):
        """
        Return all information of a single message.
        """
        message = self.db_handler.get_message(message_id)
        if message != {} or message != None:
            return {'Message': message}, 200
        else:
            return {"Message": "No messages with id:"+message_id}, 404

    @jwt_required
    def delete(self, message_id):
        """
        Delete a message with the given ID.
        """
        if check_authorization() == 1:
            response = self.db_handler.delete_message(message_id)
            if resposnse == None:
                return {"Error": "Error during data handling"}
            else:
                return {"Message": response}
        else:
            return {"Error" : "Unauthorized"}, 401

class MessageSeen(Resource):
    """
    Handles marking messages seen by certain users.
    """

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt

    def get(self, message_id, seen_id):
        """
        When this get message is processed,
        mark the message_id read by user_id.
        """
        # TODO: magic pixel handling

def check_authorization(self, user_id):
    if get_jwt_identity() == "admin":
        return 1
    else:
        return 0