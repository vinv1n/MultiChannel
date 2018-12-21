from flask import request
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep
from flask_jwt_extended import jwt_required, get_jwt_identity
<<<<<<< HEAD
import logging
=======
>>>>>>> a9891309d334c93fa43db1113629ed076c8eb117


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
            if payload["admin"] == True:
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
        response = self.db_handler.get_users(self.check_authorization())
        if response == None:
            return {"Error" : "Error during data handling"}, 400
        else:
            return {"Users": response}, 200


    def post(self):
        """ Post a new user to the database. Make a dictionary to pass to the db_handler."""

        user_data = {}
        try:
            data = request.get_json()

            user_data["username"] = data.get("username")
            user_data["password"] = pbkdf2_sha256.encrypt(saslprep(data.get("password")), rounds=200000, salt_size=16)
            user_data["preferred_channel"] = data.get("preferred_channel")
            user_data["channels"] = data.get("channels")
            user_data["admin"] = False
        except Exception as e:
            return {'Error' : "Malformed request / Error parsing data"}, 400

        response = self.db_handler.create_user(user_data)
    

        if response == "used":
            return {'Error' : "Username already in use"}, 400
        elif response == None:
            return {"Error" : "Error during data handling"}
        else:
            return {"Message" : "User created","user_id": response}, 200



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
            if payload["admin"] == True:
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
        if self.check_authorization(user_id) == True:
            response = self.db_handler.get_user(user_id)
            if response == None:
                return {"Error":"Error during data handling"}, 400
            else:
                return {"User": response}, 200
        else:
            return{"Error": "Unauthorized"}, 401
        
    
    @jwt_required
    def patch(self, user_id):
        if self.check_authorization(user_id) == True:
            data = request.get_json()
            user_data = {}
            for key in data:
<<<<<<< HEAD
                if key == "admin" and self.check_admin() != True and data[key] not in [True,False]:
                        return {"Error": "Admin field should be True or False. Olnly admin can modify this value."}, 400
=======
                if key == "admin":
                    if self.check_admin != True:
                        return {"Error": "Not modified. Only administrator can change admin flag"}, 400
>>>>>>> a9891309d334c93fa43db1113629ed076c8eb117
                elif key == "username":
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
        if self.check_authorization(user_id) == True:
            response = self.db_handler.delete_user(user_id)
            if response == None:
                return {"Error": "Error during data handling"}, 400
            elif response == True:
                return {"Message" : "User deleted"}
            return {"Message": response}
        else:
            return{"Error": "Unauthorized"}, 401
