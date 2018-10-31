import socket
import json
import logging

from socket import AF_INET, SOCK_STREAM


class IRC:

    def __init__(self, address, channels=None, nickname=None):
        self.running = False
        self.database = None  #database to save messages

        # connection
        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.port = 6667
        self.server = "IRCnet"
        self.address = address
        self.host = "IRC"

        # Bot's credentials
        if nickname:  # bot's nick
            self.nickname = nickname
        else:
            self.nickname = "MultiChannelBot"  # default

        self.user = [""]  # user of server
        self.realname = "MultiChannelBot"

        # channels that bot is joined
        if channels:
            self.default_channels = channels
        else:
            self.default_channels = []

    def connect_to_server(self):
        """
        Creates connection to IRC server

        :return: True if connection to server was succesful, otherwise False
        """
        try:
            self.socket.connect((self.address, self.port))

            # login to server
            self.socket.send("USER {} a a {}\r\n".format(self.user, self.realname).encode("utf-8"))
            # define nick
            self.socket.send("NICK {}\n".format(self.nickname).encode("utf-8"))

            if self.default_channels:
                self.socket.send("JOIN {}\n".format(self.default_channels).encode("utf-8"))

            return True  # connection was succesful
        except Exception as e:
            print("Error during connection. Error {}".format(e))
            return False

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

    @staticmethod
    def _parse_message(message):
        """
        Parses massege body and makes is correct format for irc.

        :param message: message to be parsed
        :return: parsed message string
        """
        return None

    def send_message_to_channel(self, channels, msg):
        # Db entry should be made here
        return None

    def send_message_to_user(self, users, msg):
        return None

    def receive_message(self):
        """
        Catches messages that are sent to the bot

        :return: received message data
        """
        # TODO check if there is better format for the messages
        # also other response handling probably should be done here
        data = self.socket.recv(4096).decode('utf-8').split('\r\n')
        if "PING" in data:
            self._response_to_ping(data)

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
        self.running = True
        while self.running:
            msg = self.receive_message()

