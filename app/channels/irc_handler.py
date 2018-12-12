"""
Message handler for IRC api
"""
import logging
from utils import Message, Networking

logger = logging.getLogger(__name__)

networking = Networking()  # class that handles requests

def send_message(message):
    """
    :param message: instance of message class
    :return: True if message was send succesfully, otherwise False
    """
    if not isinstance(message, Message):
        logger.critical("Message was not instance of class {{%s}}", Message.__class__)
        return False

    # TODO hide this
    # url to irc endpoint
    url = "127.0.0.1:8000/send/"

    response = networking.make_post_request(headers=message.as_dict(), url=url)
    if not response:
        return False

    return True

def get_message(message):
    if not isinstance(message, Message):
        logger.critical("Message was not instance of class {{%s}}", Message.__class__)
        return False

    # TODO hide this
    # url to irc endpoint
    url = "127.0.0.1:8000/messages/"

    response = networking.make_get_request(headers="{'id': {%s}}".format(message.get_message_id()), url=url)
    if not response:
        return False

    return True
