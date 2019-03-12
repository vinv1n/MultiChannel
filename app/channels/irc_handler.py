"""
Message handler for IRC api
"""
import logging
import requests
from utils import get_user

logger = logging.getLogger(__name__)

URI = "0.0.0.0:8000"

class IRC:

    def __init__(self, database):
        self.db = database

    def send_message(self, message, users):
        """
        :param message: instance of message class
        :return: True if message was send succesfully, otherwise False
        """

        # TODO hide this
        # url to irc endpoint
        url = "{}/{}".format(URI, "send/")

        results = []
        for user in users:
            nick = user.get("channels").get("irc").get("nickname")
            if not nick:
                continue

            data = {
                "receiver": nick,
                "message_id": message.get("_id"),
                "message": message.get("message")
            }

            response = requests.post(url, data=data)
            if response.status_code != 200:
                continue

            results.append(user)

        return results

    def get_message(self, message_id):
        # TODO hide this
        # url to irc endpoint
        url = "{}/messages/{}".format(URI, message_id)

        response = requests.get(url=url).json().get("result")

        for ans in response:
            user = ans.get("user")
            user_id = self.db.get_user_name(user)

            answer = ans.get("answer")

            self.db.add_answer_to_message(message_id, user_id, answer)
        if not response:
            return False

        return True

    def get_updates(self):
        url = "{}/{}".format(URI, "messages/")
        responses = requests.get(url=url).json().get("result")
        users = self.db.get_users()
        for response in responses:
            irc_nick = response.get(user)
            if not user:
                continue

            answer = response.get("message")
            results = []
            for user in users:
                nick = user.get("channels").get("irc").get("nickname")
                if nick == irc_nick:
                    user_id = user.get("_id")
                    message_id = response.get("message_id")
                    self.db.add_answer_to_message(message_id, user_id, answer)

                    results.append(user)

        return results