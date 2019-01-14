import json

"""
Json validation schemas for different uses

"""


def get_login_validation_schema():
    # TODO: determine maxlength of strings
    login_schema = {
        "required": ['password', 'username'],
        "properties": {
            "username": {'type': 'string', 'minLength': 4, 'maxLength': 50},
            "password": {'type': 'string', 'minLength': 6, 'maxLength': 50}
        }
    }
    return login_schema
