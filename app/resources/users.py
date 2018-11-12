import json

from flask_restful import Resource

""""
Users resource class. This class should handle everything
related to users. Trys to keep __init__.py clean.
"""
from app.database.db_handler import database_handler

class Users(Resource):
    """
    Resource to get and add users.
    """

    @staticmethod
    def get():
        p = database_handler().create_user({"foo": "bar"})
        return {"foo": str(p)}

    @staticmethod
    def post():
        return {}


class UsersSingle(Resource):
    """
    Resource for getting, updating and deleting single users.
    """

    @staticmethod
    def get(user_id):
        return {}

    @staticmethod
    def patch(user_id):
        return {}

    @staticmethod
    def delete(user_id):
        return {}
