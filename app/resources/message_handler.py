"""
Message_handler class handles the logic of piping the message
through different channels to the users.

The channels are expected to behave as functions.
The input parameters of a channel function are:


body: The text which is being sent.
type: a string describing what type of a message is being sent.
group_message: boolean value.
user: the ID of user who the message is being sent to.
channel_information: a dictionary containing all needed information
to handle the message sending. This is, for example, the user's email address.

Channel function should return whether the sending was succesful or not.

"""

from app.database.db_handler import database_handler
import json
import logging

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

    def send_message(self, message, users):
        """
        Send the message to the users using their preferred channels.
        :param dictionary message: New message that is sent.
        :param list users: List of user IDs who the message is sent to.
        """
        _message = form_message(message, users)
        # Insert the newly created message into database
        message_id = self._database_handler.create_message(message_data=_message)
        if message_id is None:
            # TODO: how to handle if message insertion fails?
            return

        user_informations = self._get_user_informations(users)

        for user_id, information in user_informations.items():
            preferred_channel = information.get('preferred_channel')
            if preferred_channel is None:
                # TODO: what to do if no channel is preferred?
                pass

            # TODO please add information why this HACK is done
            _information = json.loads(information['channels'].replace("'", '"'))# HACK!!
            channel_information = _information.get(preferred_channel)
            # channel_information = information['channels'].get(preferred_channel)
            if channel_information is None:
                # TODO: how to handle if no channel information?
                pass

            try:
                success = self._send_message_to_user(
                    message=_message,
                    user=user_id,
                    channel=preferred_channel,
                    channel_information=channel_information,
                )
            except Exception as e:  # TODO: Handle error somehow smarter
                log.debug("Message could not be sent. Reason: %s", e)
                success = False
            if success:
                self._set_message_sent_for_user(user=user_id)
        return message_id

    def _get_user_informations(self, users):
        """
        :param list users: list of user IDs whose information is retrieved
        :return: Dictionary with user ID as key, and their info as value.
                 Value is none, if no information was retrieved for that ID.
        """
        user_informations = dict()
        for user in users:
            information = self._database_handler.get_user(user_id=user)
            user_informations[user] = information

        return user_informations

    def _send_message_to_user(self, message, user, channel, channel_information):
        """
        Send the message to the user through the given channel.
        :param dictionary message: Message
        :param string user: the ID of the user.
        :param string channel: Name of the channel which is used.
        :param dictionary channel_information: Channel related information of the user.
        :return: True if sending was succesful, False otherwise.
        """
        channel = self.channels.get(channel)
        if channel is None:
            # TODO: what is the correct reaction when the channel doesn't exist?
            return
        message_type = message.get('type')
        if message_type is None:
            # TODO: handle missing type
            return
        body = message.get('body')
        group_message = message.get('group_message')

        success = channel(body, message_type, group_message, user, channel_information)
        return success

    def _set_message_sent_for_user(self, user):
        # TODO: this, use the database_handler
        pass


def form_message(message, users):
    receivers = dict()
    for user in users:
        receivers[user] = {'sent': False, 'seen': False, 'answer': ''}
    formed_message = {
        'body': message['body'],
        'type': message['type'],
        'group_message': message['group_message'],
        'receivers': receivers,
    }
    return formed_message
