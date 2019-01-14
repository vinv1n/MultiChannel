import json

"""
Json validation schemas for different uses

"""

# not actually used
LOGIN_SCHEMA = {
    "required": ['password', 'username'],
    "properties": {
        "username": {'type': 'string', 'minLength': 4, 'maxLength': 50},
        "password": {'type': 'string', 'minLength': 6, 'maxLength': 50}
    }
}


