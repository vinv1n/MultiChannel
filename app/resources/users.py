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
        response = self.db_handler.get_users()
        if response == None:
            return {"Error" : "Error during data handling"}, 400
        else:
            return {"Users": response}, 200


    def post(self):
        """ Post a new user to the database. Make a dictionary to pass to the db_handler.

      	{
	"username": "User",
	"password": "secrut",
	"preferred_channel": "email",
	"email": "adderss@server.fi",
	"facebook":"user",
	"telegram": "user",
	"irc": {"username": "user", "network": "user"},
	"slack": {"channel": "user","username": "user"}
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
        elif response == None:
            return {"Error" : "Error during data handling"}
        else:
            return {"user_id": response}, 200



class UserSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """
    def check_authorization(self, user_id):
        try:
            user = self.db_handler.get_user(user_id)
            if get_jwt_identity() in [user["username"], "admin"]:
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
        if self.check_authorization(user_id) == 1:
            response = self.db_handler.get_user(user_id)
            if response == None:
                return {"Error":"Error during data handling"}, 400
            else:
                return {"User": response}, 200
        else:
            return{"Error": "Unauthorized"}, 401
        
    
    @jwt_required
    def patch(self, user_id):
        if self.check_authorization(user_id) == 1:
            data = request.get_json()
            user_data = {}
            for key in data:
                if key == "username":
                    return {"Error": "Not modified. Cannot modify username"}, 400
                elif key == "preferred_channel":
                    if data[key] not in ["email", "slack", "irc", "facebook", "telegram"]:
                        return {"Error": "Not modified. Channel unknown"}, 400
                elif key == "password":
                    user_data[str(key)]= pbkdf2_sha256.encrypt(saslprep(data["password"]), rounds=200000, salt_size=16)
                user_data[str(key)] = data.get(key)
            response = self.db_handler.update_user(user_data, user_id)
            
            if response == 200:
                return {"Message":"modified"}, response
            else:
                return {"Error": "Not modified"}, response
        else:
            return{"Error": "Unauthorized"}, 401


    @jwt_required
    def delete(self, user_id):
        if self.check_authorization(user_id) == 1:
            response = self.db_handler.delete_user(user_id)
            if response == None:
                return {"Error": "Error during data handling"}, 400
            return {"Message": response}
        else:
            return{"Error": "Unauthorized"}, 401

    
   
