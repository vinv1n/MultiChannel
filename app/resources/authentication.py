from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep

class Login(Resource):

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username",location="json",required=True)
        parser.add_argument("password",location="json",required=True)
        args = parser.parse_args()

        user = self.db_handler.get_user_name(args["username"])
        if not user:
            return {"message": "No user: "+args["username"]},404
        else:
            if pbkdf2_sha256.verify(saslprep(args["password"]), user["password"]):
                try:
                    access_token = create_access_token(identity = user["username"])
                    return {"message": "new token created", "access_token": access_token}
                except Exception as e:
                    return {"message": "Error creating token"+str(e)}
            else:
                return {"message": "Authentication error"}
