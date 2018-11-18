from flask import request
from flask_restful import Resource
import json


class Users(Resource):
    """
    Resource to get and add users.
    """
    def __init__(self, **kwargs):
        self.db_handler = kwargs['db_handler']


    def get(self):
        response = self.db_handler.get_users()
        return {"Users" : response}

    @staticmethod
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
        try:
            data = request.get_json()

            user_data["username"] = data.get("username")
            user_data["password"] = data.get("password")
            user_data["preferred_channel"] = data.get("preferred_channel")
            user_data["channels"] = data.get("channels")
        except Exception as e:
            return {}, 400

        response = self.db_handler.create_user(user_data)
        return {"user_id": response}


class UsersSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """
    def __init__(self, **kwargs):
        self.db_handler = kwargs['db_handler']


    def get(self, user_id):
        response = self.db_handler.get_user(user_id)
        return {"User" : response }


    def patch(self, user_id):
        data = request.get_json()
        user_data = {}
        for key in data:
            user_data[str(key)] = data.get(key)
        response = self.db_handler.update_user(user_data, user_id)
        return {}, response

    def delete(self, user_id):
        response = self.db_handler.delete_user(user_id)
        return {"Users" : response }
