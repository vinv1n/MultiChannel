import urllib3
import logging
import pprint
import json

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

        self.token = args[0]
        self.base_url = "https://api.telegram.org/bot{}/".format(self.token)

        # database handler
        self.database = kwargs.get("database_handler")

        # for requests
        self.http = urllib3.PoolManager()

    def send_message(self, message):
        """
        TODO make the bot accept private messages
 
        Send message to channels or users
        :param msg: message string
        :param parameters: parameters for query strings
        :return: status code and response body
        """
        response, status = self._make_request(request_type="POST", command=BOT_COMMANDS.get("send_message"),
                                                parameters={"text": message.body, "chat_id": message.receivers})

        return response, status

    def get_updates(self):
        """
        Get messages that are send to the bot
        :return: response status_code, response body
        """
        status, response = self._make_request(request_type="GET", command=BOT_COMMANDS.get("updates"))
        return response, status

    def _make_request(self, request_type, command, parameters=None):
        """
        Make http request to telegram api
        :param request_type: POST or GET method
        :param command: Telegram api endpoints
        :param parameters: query string parameters for some endpoints
        :return: response data and response status code
        """
        if parameters:
            _url = self._create_query_string(command=command, parameters=parameters)
        else:
            _url = "{}{}".format(self.base_url, command)

        response = self.http.request(request_type, _url)

        return {response.data}, response.status

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
