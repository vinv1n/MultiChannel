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

user_schema={
            'type': 'object',
                'properties':{
                    'username':{ 'type': 'string', 'minLength': 4, 'maxLength': 20 },
                    'password':{ 'type': 'string', 'minLength': 4, 'maxLength': 32 },
                    'preferred_channel':{ 'type': 'string', 'enum': ['email','telegram','irc'] },
                    'channels':{'type':'object', 'properties':{
                        
                        'email': {'type':'object','properties':{
                            'address': {'type': 'string'}},
                            'required': ['address'],'additionalProperties': False},

                        'telegram': {'type':'object','properties':{
                            'user_id':{'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},

                        'irc': {'type':'object','properties':{
                            'nickname':{'type': 'string'},
                            'network':{'type': 'string'}},
                            'required': ['nickname','network'],'additionalProperties': False},
							
                    },'required': ['email','telegram','irc'],'additionalProperties': False}
                },
                'required': [ 'username', 'password', 'preferred_channel', 'channels' ],
                'additionalProperties': False
        }

user_patch_schema={
            'type': 'object',
                'properties':{
                    'password':{ 'type': 'string', 'minLength': 4, 'maxLength': 32 },
                    'preferred_channel':{ 'type': 'string', 'enum': ['email','telegram','irc'] },
                    'channels':{'type':'object', 'properties':{
                        
                        'email': {'type':'object','properties':{
                            'address': {'type': 'string'}},
                            'required': ['address'],'additionalProperties': False},

                        'telegram': {'type':'object','properties':{
                            'user_id':{'type': 'string'}},
                            'required': ['user_id'],'additionalProperties': False},

                        'irc': {'type':'object','properties':{
                            'nickname':{'type': 'string'},
                            'network':{'type': 'string'}},
                            'required': ['nickname','network'],'additionalProperties': False},
							
                    },'required': ['email','telegram','irc'],'additionalProperties': False}
                },
                'additionalProperties': False
        }
		
		
message_schema={
            'type': 'object',
                'properties':{
                    'message':{ 'type': 'string', 'minLength': 2, 'maxLength': 500 },
                    'sender':{ 'type': 'string', 'minLength': 4, 'maxLength': 20 },
                    'users':{ 'type': 'array', 'contains':{'type':'string'} },
                    'type':{ 'type': 'string', 'enum':['fnf','answerable', 'traced'] },
                    'group_message':{ 'type': 'string', 'enum':['True', 'False'] }

                },
                'required': [ 'message', 'users', 'sender', 'type', 'group_message' ],
                'additionalProperties': False
    }
