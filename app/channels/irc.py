import socket
import json
import logging
import pprint

from socket import AF_INET, SOCK_STREAM

log = logging.getLogger(__name__)


class IRC:

    def __init__(self, channels=None, nickname=None):
        self.running = False
        self.database = None  #database to save messages

        # connection
        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.port = 6667
        self.address = "irc.nebula.fi"

        # Bot's credentials
        if nickname:  # bot's nick
            self.nickname = nickname
        else:
            self.nickname = "MultiChannelBot"  # default

        self.bot_name = "MultiChannelBot"  # used for realname and username

        # channels that bot is joined
        if channels:
            self.default_channels = channels
        else:
            self.default_channels = ["#vinvin.bot"]  # FIXME

    def connect_to_server(self):
        """
        Creates connection to IRC server

        :return: True if connection to server was succesful, otherwise False
        """
        try:
            self.socket.connect((self.address, self.port))
            # login to server
            self.socket.send("USER {} a a {}\r\n".format(self.bot_name, self.bot_name).encode("utf-8"))
            # define nick
            self.socket.send("NICK {}\r\n".format(self.nickname).encode("utf-8"))

            #if self.default_channels:
            #    self._join_channels(self.default_channels)
            self.socket.send("JOIN {}\r\n".format(self.default_channels[0]).encode("utf-8"))

            return True  # connection was succesful
        except Exception as e:
            log.critical("Error during connection. Error %s", e)
            return False

    def _join_channels(self, channels):
        for channel in channels:
            if channel not in self.default_channels:
                self.socket.send("JOIN {}\n".format(channel).encode("utf-8"))
                self.default_channels.append(channel)

    def _response_to_ping(self, msg):
        """
        Responses to server when ping is asked.

        :param msg: Received message
        """
        self.socket.send("PONG {}\r\n".format(msg[1]).encode('utf-8'))

    def is_running(self):
        """
        Tells if bot is running in instance

        :return: False if bot is not running, otherwise True
        """
        return self.running

    def get_channels(self):
        return self.default_channels

    @staticmethod
    def _parse_message(message):
        """
        Parses massege body and makes is correct format for irc.

        :param message: message to be parsed
        :return: parsed message string
        """
        return ""

    def send_message_to_channel(self, channels, msg):

        parsed_message = IRC._parse_message(msg)

        for channel in channels:
            if channel not in self.default_channels:
                self._join_channels([channel])

            self.socket.sendall("PRIVMSG {} {}\r\n".format(channel, parsed_message).encode("utf-8"))

        # TODO add db entry and error handling
        return True

    def send_message_to_user(self, users, msg):
        """
        Sents message to to all selected users.

        :param users: List of users that message should be sent
        :param msg: Message which will be sent
        """
        parsed_message = IRC._parse_message(msg)

        for user in users:
            self.socket.sendall("PRIVMSG {} {}\r\n".format(user, parsed_message).encode("utf-8"))

        # TODO add db entry and error handling
        return True

    def receive_message(self):
        """
        Catches messages that are sent to the bot

        :return: received message data
        """
        # TODO check if there is better format for the messages
        # also other response handling probably should be done here
        data = self.socket.recv(4096).decode('utf-8').split('\r\n')
        if log.isEnabledFor(logging.DEBUG):
            log.debug("%s", pprint.pformat(data))
        log.warning(data)
        if "PING" in data:
            self._response_to_ping(data)
            return data

        return data

    def _determine_if_msg_recived(self, users):
        """
        Determines if user has received the message.

        :param users: users that message has been sent
        :return: dict containing user status
        """
        return None

    def run(self):
        """
        """
        self.connect_to_server()
        self.running = True
        while self.running:
            msg = self.receive_message()
            log.warning(msg)

