import logging
import uuid
import six
import json
import functools

from flask import render_template, request, abort
from jsonschema import validate, ValidationError

if six.PY2:
    import urllib
else:
    import urllib3 as urllib

logger = logging.getLogger(__name__)


class MultiChannelException(Exception):
    """
    Custom exeption class for MultiChannel app
    """
    def __init__(self, message):
        super().__init__(message)


def get_user(user_id, users):
    """
    Returns given user id from all id
    """
    for user in users:
        _id = user.get("_id")
        if _id == user_id:
            return user

    return {}


class Message:
    """
    Message class containing all information about messages.
    This class should make same everywhere.
    """

    def __init__(self, body, message_type, sender, channel_information, receivers):
        self._id = uuid.uuid4()  # create random id for message
        self.messge_body = body
        self.message_type = message_type
        self.sender = sender
        self.channel = channel_information

        # determine if message is group message
        if len(receivers) > 1:
            self.group_message = True
        else:
            self.group_message = False

        self.receivers = receivers


    @classmethod
    def create_message(cls, body, message_type, group_message, user, channel_information):
        message = cls(body, message_type, group_message, user, channel_information)
        return message

    def as_dict(self):
        try:
            message_dict = self._form_message()
            return message_dict
        except (ValueError, AttributeError) as e:
            logger.critical("Dictionary could not be created. Reason: %s", e)
            return None

    def get_sender(self):
        return self.sender

    def get_message_id(self):
        # TODO: some hashing would be nice
        return str(self._id, errors="ignore")

    def _form_message(self):
        receivers = {}
        for rc in self.receivers:
            receivers[rc] = {'sent': False, 'seen': False, 'answer': ''}

        formed_message = {
            'id': self.get_message_id(),
            'body': self.messge_body,
            'type': self.message_type,
            'group_message': self.group_message,
            'receivers': receivers,
        }
        return formed_message


class Networking:
    def __init__(self, *args, **kwargs):
        self._pool = urllib.PoolManager()

    def make_post_request(self, headers, url, args=None):
        if not isinstance(args, dict):
            raise ValueError("Incorrect args type")

        if args:
            response = self._pool.request(method="POST", url=url, fields=args, headers=headers)
        else:
            response = self._pool.request(method="POST", url=url, headers=headers)

        return self._decode_response(response=response)

    def make_get_request(self, headers, url, args=None):
        if not isinstance(args, dict):
            raise ValueError("Incorrect args type")

        if args:
            response = self._pool.request(url=url, method="GET", fields=args, headers=headers)
        else:
            response = self._pool.request(url=url, method="GET", headers=headers)

        return self._decode_response(response=response)

    @staticmethod
    def _decode_response(response):
        response_json = None
        try:
            response_json = json.loads(response.decode("utf-8"))
        except ValueError:
            return None, 400

        return response_json, 200

def json_validator(*validator):
    def decorator_json_validator(func):
        @functools.wraps(func)
        def wrapper_json_validator(*args, **kwargs):
            result_json = request.get_json()
            logger.critical(result_json)
            try:
                validate(validator[0], result_json)
            except (ValidationError, AttributeError) as e:
               return render_template("validation_error.html"), e
            return func(*args, **kwargs)
        return wrapper_json_validator

    return decorator_json_validator

def encode_string(string):
    return string.decode("utf-8")
