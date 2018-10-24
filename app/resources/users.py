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