"""
Message handler for IRC api
"""
import logging
import requests
from utils import get_user

logger = logging.getLogger(__name__)

class IRC:

    def __init__(self, database):
        self.db = database

    def send_message(self, message, user, users, info):
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
            user_info = get_user(user, users)
            nick = user_info.get("channels").get("irc").get("nickname")
            if not nick:
                continue

            data = {
                "receiver": nick,
                "message_id": message.get("_id"),
                "message": message.get("message")
            }

            response = requests.post(url, data=data)
            result.append(response.json())

        if not result:
            return False

        return True

    def get_message(self, message_id):
        # TODO hide this
        # url to irc endpoint
        url = "127.0.0.1:8000/messages/{}".format(message_id)

        response = requests.get(url=url).json().get("result")

        for ans in response:
            user = ans.get("user")
            user_id = self.db.get_user_name(user)

            answer = ans.get("answer")

            self.db.add_answer_to_message(message_id, user_id, answer)
        if not response:
            return False

        return True
