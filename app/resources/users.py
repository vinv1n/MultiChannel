from flask import request
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep
from flask_jwt_extended import jwt_required, get_jwt_identity


""""
Users resource class. This class should handle everything
related to users. Trys to keep __init__.py clean.
"""


class Users(Resource):
    
    """
    Resource to get and add users.
    """

    def check_authorization(self, user_id):
        try:
            user = self.db_handler.get_user(user_id)
            if get_jwt_identity() == "admin":
                return 1
            else:
                return 0
        except Exception as e:
            return 0
    
    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt
    
    @jwt_required
    def get(self):
        self.check_authorization()
        response = self.db_handler.get_users()
        return {"Users": response}


    def post(self):
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
        channels = {
            "email": {"address": ""},
            "facebook": {"user_id": ""},
            "telegram": {"user_id": ""},
            "irc": {"username": "", "network": ""},
            "slack": {"channel": "","username": ""}
           }
        try:
            data = request.get_json()
        except Exception as e:
            return {'Error' : "Malformed request"}, 400

        try:
            user_data["username"] = data["username"]
            user_data["password"] = pbkdf2_sha256.encrypt(saslprep(data["password"]), rounds=200000, salt_size=16)
            user_data["preferred_channel"] = data["preferred_channel"]
            channels["email"]["address"] = data["email"]
            channels["facebook"]["user_id"] = data["facebook"]
            channels["facebook"]["user_id"] = data["telegram"]
            channels["irc"]["username"] = data["irc"]["username"]
            channels["irc"]["network"] = data["irc"]["network"]
            channels["slack"]["username"] = data["slack"]["username"]
            channels["slack"]["channel"] = data["slack"]["channel"]
            user_data["channels"] = channels
        except Exception as e:
            return {"Error": "Error parsing data"+str(e)
            }, 400
                
        response = self.db_handler.create_user(user_data)
        if response == "Username already in use":
            return {'Error' : "Username in use"}, 400
        else:
            return {"user_id": response}, 200



class UserSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """
    def check_authorization(self, user_id):
        try:
            user = self.db_handler.get_user(user_id)
            if get_jwt_identity() == response["username"] or "admin":
                return 1
            else:
                return 0
        except Exception as e:
            return 0

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt

    @jwt_required
    def get(self, user_id):
        if self.check_authorization == 1:
            response = self.db_handler.get_user(user_id)
            return {"User": response}
        else:
            return{"Error": "Unauthorized"}, 401
        
    
    @jwt_required
    def patch(self, user_id):
        if self.check_authorization == 1:
            data = request.get_json()
            user_data = {}
            for key in data:
                user_data[str(key)] = data.get(key)
            response = self.db_handler.update_user(user_data, user_id)
            return {}, response
        else:
            return{"Error": "Unauthorized"}, 401
    @jwt_required
    def delete(self, user_id):
        if self.check_authorization == 1:
            response = self.db_handler.delete_user(user_id)
            return {"message": response}
        else:
            return{"Error": "Unauthorized"}, 401

    
   
