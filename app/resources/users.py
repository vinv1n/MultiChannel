from flask import request
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate

""""
Users resource class. This class should handle everything
related to users. Trys to keep __init__.py clean.
"""


class Users(Resource):

    """
    Resource to get and add users.
    """

    def check_authorization(self):
        try:
            payload = get_jwt_identity()
            if payload["admin"] is True:
                return True
            else:
                return False
        except Exception as e:
            return False

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt

    @jwt_required
    def get(self):
        authorized = self.check_authorization()
        if not authorized:
            return {"msg": "Action not authorized."}, 401
        response = self.db_handler.get_users()
        if response is None:
            return {"msg": "Error during data handling"}, 400
        else:
            return {"users": response}, 200

    def post(self):
        """ Post a new user to the database. Make a dictionary to pass to the db_handler."""

        user_schema={
            'type': 'object',
                'properties':{
                    'username':{ 'type': 'string', 'minLength': 4, 'maxLength': 20 },
                    'password':{ 'type': 'string', 'minLength': 4, 'maxLength': 32 },
                    'preferred_channel':{ 'type': 'string', 'enum': ['email','facebook','telegram','irc','slack'] },
                    'channels':{'type':'object', 'properties':{
                        
                        'email': {'type':'object','properties':{
                            'address': {'type': 'string'}},
                            'required': ['address'],'additionalProperties': False},
                        
                        
                        'facebook': {'type':'object','properties':{
                            'user_id': {'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},


                        'telegram': {'type':'object','properties':{
                            'user_id':{'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},

                        'irc': {'type':'object','properties':{
                            'nickname':{'type': 'string'},
                            'network':{'type': 'string'}},
                            'required': ['nickname','network'],'additionalProperties': False},

                        'slack': {'type':'object','properties':{
                            'username':{'type': 'string'},
                            'channel':{'type': 'string'}},
                            'required': ['username','channel'],'additionalProperties': False}
                    },'required': ['email','facebook','telegram','irc','slack'],'additionalProperties': False}
                },
                'required': [ 'username', 'password', 'preferred_channel', 'channels' ],
                'additionalProperties': False
        }

        try:
            validate(request.json,user_schema)
        except Exception as e:
            error_msg = str(e).split("\n")
            return {"msg": "error with input data:"+ str(error_msg[0])}, 400

        user_data = {}
        data = request.get_json()
        user_data["username"] = data.get("username")
        user_data["password"] = pbkdf2_sha256.encrypt(saslprep(data.get("password")), rounds=200000, salt_size=16)
        user_data["preferred_channel"] = data.get("preferred_channel")
        user_data["channels"] = data.get("channels")
        user_data["admin"] = False

        response = self.db_handler.create_user(user_data)

        if response == "used":
            return {'msg': "Username already in use"}, 400
        elif response is None:
            return {"msg": "Error during data handling"}
        else:
            return {"msg": "User created", "user_id": response}, 200


class UserSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """
    def check_authorization(self, user_id):

        try:
            user = self.db_handler.get_user(user_id)
            payload = get_jwt_identity()
            if payload["admin"] == True or payload["username"] == user["username"]:
                return True
            else:
                return False
        except Exception as e:
            return 0

    def check_admin(self):
        try:
            payload = get_jwt_identity()
            if payload["admin"] is True:
                return True
            else:
                return False
        except Exception as e:
            return 0

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt

    @jwt_required
    def get(self, user_id):
        if self.check_authorization(user_id) is True:
            response = self.db_handler.get_user(user_id)
            if response is None:
                return {"msg": "Error during data handling"}, 400
            else:
                return {"User": response}, 200
        else:
            return{"msg": "Unauthorized"}, 401

    @jwt_required
    def patch(self, user_id):
        user_schema={
            'type': 'object',
                'properties':{
                    'password':{ 'type': 'string', 'minLength': 4, 'maxLength': 32 },
                    'preferred_channel':{ 'type': 'string', 'enum': ['email','facebook','telegram','irc','slack'] },
                    'channels':{'type':'object', 'properties':{
                        
                        'email': {'type':'object','properties':{
                            'address': {'type': 'string'}},
                            'required': ['address'],'additionalProperties': False},
                        
                        
                        'facebook': {'type':'object','properties':{
                            'user_id': {'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},


                        'telegram': {'type':'object','properties':{
                            'user_id':{'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},

                        'irc': {'type':'object','properties':{
                            'nickname':{'type': 'string'},
                            'network':{'type': 'string'}},
                            'required': ['nickname','network'],'additionalProperties': False},

                        'slack': {'type':'object','properties':{
                            'username':{'type': 'string'},
                            'channel':{'type': 'string'}},
                            'required': ['username','channel'],'additionalProperties': False}
                    },'additionalProperties': False}
                },
                'additionalProperties': False
        }
        try:
            validate(request.json,user_schema)
        except Exception as e:
            error_msg = str(e).split("\n")
            return {"msg": "error with input data:"+ str(error_msg[0])}, 400

        if self.check_authorization(user_id) is True:
            data = request.get_json()
            user_data = {}
            for key in data:
                if key == "admin" and self.check_admin() != True and data[key] not in [True,False]:
                        return {"Error": "Admin field should be True or False. Olnly admin can modify this value."}, 400
                elif key == "username":
                    return {"Error": "Not modified. Cannot modify username"}, 400
                elif key == "preferred_channel":
                    if data[key] not in ["email", "slack", "irc", "facebook", "telegram"]:
                        return {"Error": "Not modified. Channel unknown"}, 400
                if key == "password":
                    user_data[str(key)] = pbkdf2_sha256.encrypt(saslprep(data["password"]), rounds=200000, salt_size=16)
                else:
                    user_data[str(key)] = data.get(key)
            response = self.db_handler.update_user(user_data, user_id)

            if response == 200:
                return {"msg": "modified"}, response
            else:
                return {"msg": "Not modified"}, response
        else:
            return{"msg": "Unauthorized"}, 401

    @jwt_required
    def delete(self, user_id):
        if self.check_authorization(user_id) is True:
            response = self.db_handler.delete_user(user_id)
            if response is None:
                return {"msg": "Error during data handling"}, 400
            elif response is True:
                return {"msg": "User deleted"}
            return {"msg": response}
        else:
            return{"msg": "Unauthorized"}, 401
