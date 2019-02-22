"""
Message_handler class handles the logic of piping the message
through different channels to the users.

The channels are expected to behave as functions.
The input parameters of a channel function are:

users: a list of users and their information, who have chosen the channel
as their preferred one.
message: the message to be sent to the users.

Channel function should return a list of user IDs who the channel managed to send the message to.
"""

from app.database.db_handler import database_handler
import logging
from utils import Message

log = logging.getLogger(__name__)


class Message_handler:
    """
    Handles the logic of seding messages to different channels.
    """
    def __init__(self, channels, _database_handler=None):
        """
        :param dictionary channels: key is the channel name,
        value the channel function to be called.
        """
        self.channels = channels
        if _database_handler is None:
            self._database_handler = database_handler()
        else:
            self._database_handler = _database_handler

    def send_message(self, message):

        """Send the message to the users using their preferred channels.
        :param dictionary message: New message that is sent.
        """
        _message = form_message(message)
        # Insert the newly created message into database
        message_id = self._database_handler.create_message(message_data=_message)
        if message_id is None:
            return None, None
        _message['_id'] = message_id

        users = self._database_handler.get_users()
        users_who_received_the_message = list()
        skipped_channels = list()
        for channel_name, channel in self.channels.items():
            users_of_channel = [
                user for user in users
                if user.get('preferred_channel') == channel_name
            ]
            if len(users_of_channel) == 0:
                continue
            try:
                received_message = channel.send_message(_message, users_of_channel)
                users_who_received_the_message = [*users_who_received_the_message, *received_message]
            except Exception as e:
                log.warning("Message could not be sent via {}. Reason: {}".format(channel_name, e))
                skipped_channels.append(channel_name)

        self._set_message_sent_for_users(message_id, users_who_received_the_message)

        if len(skipped_channels) == 0:
            msg = "Message succesfully sent via all channels"
        else:
            msg = "Failed to send the message via channels: {}".format(', '.join(skipped_channels))
        return message_id, msg

    def _set_message_sent_for_users(self, message_id, user_ids):
        try:
            successes = self._database_handler.set_message_sent(message_id, user_ids)
        except Exception as e:
            log.warning('Could not set sent status for the message: {}'.format(e))
            return False
        return successes


def form_message(message):
    receivers = dict()
    for user in message['users']:
        receivers[user] = {'sent': False, 'seen': False, 'answer': ''}
    formed_message = {
        'message': message['message'],
        'type': message['type'],
        'group_message': message['group_message'],
        'receivers': receivers,
        'timestamp': message['timestamp']
    }
    return formed_message
