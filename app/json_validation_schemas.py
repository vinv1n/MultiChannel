import json

"""
Json validation schemas for different uses

"""

# not actually used
login_schema = {
    'type': 'object',
        'properties':{
            'username':{ 'type': 'string'},
            'password':{ 'type': 'string'}
        },
        'required': [ 'username', 'password' ],
        'additionalProperties': False
}
