"""
Message handler for IRC api
"""
import logging
import requests

logger = logging.getLogger(__name__)

class IRC:

    def __init__(self, database):
        self.db = database

    def send_message(self, message, user, info):
        """
        :param message: instance of message class
        :return: True if message was send succesfully, otherwise False
        """

        # TODO hide this
        # url to irc endpoint
        url = "127.0.0.1:8000/send/"
        rc = message.get("receivers")

        result = []
        for user in rc:
            user_info = self.db.get_user(user)
            nick = user_info.get("channels").get("irc").get("nickname")
            if not nick:
                continue

            data = {
                "receiver": nick,
                "message_id": message.get("id"),
                "message": message.get("message")
            }

            response = requests.post(url, data=data)
            result.append(response.json())

        if not result:
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
