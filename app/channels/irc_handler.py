"""
Message handler for IRC api
"""
import logging
from utils import Message, Networking

logger = logging.getLogger(__name__)

networking = Networking()  # class that handles requests
class IRC:

    @staticmethod
    def send_message(body, message_type, group_message, user, channel_information):
        """
        :param message: instance of message class
        :return: True if message was send succesfully, otherwise False
        """

        # TODO hide this
        # url to irc endpoint
        url = "127.0.0.1:8000/send/"
        message = Message(body, message_type, group_message, user, channel_information)

        response = networking.make_post_request(headers=message.as_dict(), url=url)
        if not response:
            return False

        return True

    @staticmethod
    def get_message(message):
        # TODO hide this
        # url to irc endpoint
        url = "127.0.0.1:8000/messages/"

        response = networking.make_get_request(headers="{'id': {%s}}".format(message.get_message_id()), url=url)
        if not response:
            return False

        return True
