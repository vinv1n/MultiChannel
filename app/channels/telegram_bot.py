import urllib3
import logging
import pprint
import json
import uuid
import requests
import pprint

# from tokens import TELEGRAM_TOKEN

logger = logging.getLogger(__name__)

BOT_COMMANDS = {
    "status": "getMe",
    "updates": "getUpdates",
    "send_message": "sendMessage",  # chat_id and text is needed
    "send_document": "sendDocument",
    "get_member": "getChatMember",
    "get_chat_info": "getChat",
    "get_member_count": "getChatMembersCount"
}

class Telegram:

    def __init__(self, *args, **kwargs):

        if not isinstance(args[0], str):
            raise ValueError("Invalid token")

        self.active = {}

        self.token = args[0]
        self.base_url = "https://api.telegram.org/bot{}/".format(self.token)

        # database handler
        self.database = kwargs.get("database_handler")

        self._update_active()

    def send_message(self, message):
        """
        Send message to channels or users
        :param msg: message string
        :param parameters: parameters for query strings
        :return: status code and response body
        """
        # Updates all active chats
        self._update_active()

        responses = []
        for user in message.recievers:
            entry = self._make_request(request_type="POST", command=BOT_COMMANDS.get("send_message"),
                                            parameters={"text": message.message_body, "chat_id": self.active.get(user, "")})
            responses.append(entry.json())

        return responses

    def get_updates(self):
        """
        Get messages that are send to the bot
        :return: response status_code, response body
        """
        response = self._make_request(request_type="GET", command=BOT_COMMANDS.get("updates"))
        return response

    def _make_request(self, request_type, command, parameters=None):
        """
        Make http request to telegram api
        :param request_type: POST or GET method
        :param command: Telegram api endpoints
        :param parameters: query string parameters for some endpoints
        :return: response data and response status code
        """
        _url = "{}{}?".format(self.base_url, command)

        if request_type.lower() == "post":
            response = requests.post(_url, data=parameters)
        else:
            response = requests.get(_url)

        return response

    def get_bot_status(self):
        """
        """
        response, statuscode = self._make_request(request_type="GET", command=BOT_COMMANDS.get("status"))
        if statuscode != 200:
            logger.warning("Error on request error code: %s", statuscode)

        return response

    def _create_query_string(self, command, parameters):
        """
        FIXME: make lambda function to avoid for-loops
        :param parameters: dict containing paramater as key and value
        """
        query_string = "{}{}?".format(self.base_url, command)
        querys = []
        for key, item in parameters.items():
            querys.append("{}={}".format(key, item))

        query_string += "&".join(querys)
        return query_string

    def _update_active(self):
        """
        A way more compex than it needs to be

        TODO: create database table/collection for this
        """
        rjson = self.get_updates().json()
        results = rjson.get("result")

        entry = {}
        for message in results:
            msg = message.get("message")
            chat = msg["chat"]
            chat_id = chat.get("id")
            if chat_id not in self.active.values():
                if chat.get("type") == "private":
                    entry[chat.get("username")] = chat_id
                else:
                    entry[chat.get("title")] = chat_id
        if entry:
            self.active.update(entry)
