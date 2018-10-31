from flask_restful import Resource

""""
Users resource class. This class should handle everything
related to users. Trys to keep __init__.py clean.
"""


class Users(Resource):
    """
    Resource to get and add users.
    """

    @staticmethod
    def get():
        return {"man": 200}

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
