import urllib3
import logging

from tokens import TELEGRAM_TOKEN

logger = logging.getLogger(__name__)


BOT_COMMANDS = {
    "status": "getMe",
    "updates": "getUpdates",
    "send_message": "sendMessage",
    "send_document": "sendDocument",
    "get_member": "getChatMember",
    "get_chat_info": "getChat",
    "get_member_count": "getChatMembersCount"
}

class Telegram:

    def __init__(self, *args, **kwargs):
        self.base_url = "https://https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)

        self.database = kwargs.get("database_handler")

        # for requests
        self.http = urllib3.PoolManager()

    def send_message(self, msg):
        pass

    def get_updates(self):
        pass

    def _make_request(self, request_type, command, parameters=None):
        """
        """
        if command not in BOT_COMMANDS.keys():
            return {"error": "invalid bot command"}, 404

        if parameters:
            _url = self._create_query_string(command=command, parameters=parameters)
        else:
            _url = "{}{}".format(self.base_url, command)

        response = self.http.request(request_type, _url)

        return {response.data}, response.status

    def get_bot_status(self):
        """
        """
        response = self._make_request(request_type="GET", command=BOT_COMMANDS.get("status"))

        return response

    def _create_query_string(self, command, parameters):
        """
        :param parameters: dict containing paramater as key and value
        """
        query_string = "{}{}?".format(self.base_url, command)
        querys = []
        for key, item in parameters.items():
            querys.append("{}={}".format(key, item))

        query_string += "&".join(querys)
        return query_string
