import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate

class Messages(Resource):
    """
    Resource for posting, fetching and deleting messages.
    """

    def __init__(self, db_handler, message_handler, jwt):
        self.db_handler = db_handler
        self.message_handler = message_handler
        self.jwt = jwt


    def check_authorization(self):
        try:
            payload = get_jwt_identity()
            if payload["admin"] == True:
                return True
            else:
                return False
        except Exception as e:
            return False

    @jwt_required
    def get(self):
        """
        Get a list of all messages in database.
        """
        if self.check_authorization() == True:
            try:
                response = self.db_handler.get_messages()
                if response == None:
                    return {"msg": "Error during data handling"}, 400
                else:
                    return {'messages': response}, 200
            except Exception as e:
                return {"msg": "Error during data handling"}, 400
        else:
            return {"msg" : "Unauthorized"}, 401

    @jwt_required
    def post(self):
        """
        Send a new message.
        """

        message_schema={
            'type': 'object',
                'properties':{
                    'message':{ 'type': 'string', 'minLength': 2, 'maxLength': 500 },
                    'sender':{ 'type': 'string', 'minLength': 4, 'maxLength': 20 },
                    'users':{ 'type': 'array', 'contains':{'type':'string'} },
                    'type':{ 'type': 'string', 'enum':['fnf','answerable', 'traced'] },
                    'group_message':{ 'type': 'string', 'enum':['True', 'False'] }

                },
                'required': [ 'message', 'users', 'sender', 'type', 'group_message' ],
                'additionalProperties': False
    }
        try:
            validate(request.json,message_schema)
        except Exception as e:
            error_msg = str(e).split("\n")
            return {"msg": "error with input data:"+ str(error_msg[0])}, 400

        if self.check_authorization() == True:

            args = {}
            data = request.get_json()
            args['message'] = data['message']
            args['sender'] = data['sender']
            args['users'] = data['users']
            args['type'] = data['type']
            args['group_message'] = data['group_message']
            args['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            message_id, msg = self.message_handler.send_message(args)
            if message_id != None:
                return {'message_id': message_id, 'msg' : msg}
            else:
                return {'msg': 'Error. Could not post the message'}, 400
        else:
            return {'msg' : "Unauthorized"}, 401


class MessageSingle(Resource):
    """
    For handling single messages in database.
    """

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt


    def check_authorization(self):
        try:
            payload = get_jwt_identity()
            if payload["admin"] == True:
                return True
            else:
                return False
        except Exception as e:
            return False

    @jwt_required
    def get(self, message_id):
        """
        Return all information of a single message.
        """
        if self.check_authorization() == True:
            message = self.db_handler.get_message(message_id)
            if message != {} or message != None:
                return {'message': message}, 200
            else:
                return {"msg": "No messages with id:"+message_id}, 404
        else:
            return {"msg" : "Unauthorized"}, 401

    @jwt_required
    def delete(self, message_id):
        """
        Delete a message with the given ID.
        """
        if self.check_authorization() == True:
            response = self.db_handler.delete_message(message_id)
            if response == None:
                return {"msg": "Error during data handling"}
            else:
                return {"msg": response}, 200
        else:
            return {"msg" : "Unauthorized"}, 401

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