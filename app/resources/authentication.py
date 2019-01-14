from flask import request, Response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies)
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep
from jsonschema import validate


class UserLogin(Resource):

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt


   
    def post(self):

        login_schema={
            'type': 'object',
                'properties':{
                    'username':{ 'type': 'string'},
                    'password':{ 'type': 'string'}
                },
                'required': [ 'username', 'password' ],
                'additionalProperties': False
    }
        try:
            validate(request.json,login_schema)
        except Exception as e:
            error_msg = str(e).split("\n")
            return {"msg": "error with input data:"+ str(error_msg[0])}, 400

        parser = reqparse.RequestParser()
        parser.add_argument("username",location="json")
        parser.add_argument("password",location="json")
        args = parser.parse_args()


        user = self.db_handler.get_user_name(args['username'])
        if user is None:
            return {"msg": "Authentication error"}, 401
        else:
            if pbkdf2_sha256.verify(saslprep(args["password"]), user["password"]):
                try:
                    access_token = create_access_token(identity = { "username" : user["username"], "admin" : user["admin"], "_id": user["_id"]})
                    refresh_token = create_refresh_token(identity = { "username" : user["username"], "admin" : user["admin"], "_id": user["_id"]})
                    resp = jsonify({'msg': 'logged in'})
                    set_access_cookies(resp, access_token)
                    set_refresh_cookies(resp, refresh_token)
                    return resp
                except Exception as e:
                    return {"msg": "Authentication error"}, 401
            else:
                return {"msg": "Authentication error"}, 401


class Logout(Resource):

    def __init__(self, db_handler, jwt, blacklist):
        self.db_handler = db_handler
        self.jwt = jwt
        self.blacklist = blacklist

    
    @jwt_required
    def post(self):
        try:
            jti = get_raw_jwt()['jti']
            self.blacklist.add(jti)
            resp = {"msg": "Logged out"}
            unset_jwt_cookies(resp)
            return resp
        except Exception as e:
            return {"msg":"Error blacklisting token."+str(e)}, 500


class RefreshLogin(Resource):

    def __init__(self, db_handler, jwt):
        self.db_handler = db_handler
        self.jwt = jwt


    @jwt_refresh_token_required
    def post(self):
        try:
            user = get_jwt_identity()
            access_token = create_access_token(identity = user)
            resp = jsonify({'msg': 'logged in'})
            set_access_cookies(resp, access_token)
            return resp
        except Exception as e:
            return {"msg" : "Error creating token"}, 400

class RefreshLogout(Resource):

    def __init__(self, db_handler, jwt, blacklist):
        self.db_handler = db_handler
        self.jwt = jwt
        self.blacklist = blacklist

    @jwt_refresh_token_required
    def post(self):
        try:
            jti = get_raw_jwt()['jti']
            self.blacklist.add(jti)
            return {"msg": "Logged out"}, 200
        except Exception as e:
            return {"msg":"Error blacklisting token."+str(e)}, 500
