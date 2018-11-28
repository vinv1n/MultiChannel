import logging
import uuid

logger = logging.getLogger(__name__)


class MultiChannelExeption(Exception):
    """
    Custom exeption class for MultiChannel app
    """
    def __init__(self, message, error):
        super().__init__(message)



class Message:

    def __init__(self, body, message_type, sender, channel_information, receivers):
        self._id = uuid.uuid4()  # create random id for message
        self.messge_body = body
        self.message_type = message_type
        self.sender = sender
        self.channel = channel_information

        # determine if message is group message
        if len(receivers) > 1:
            self.group_message = True
        else:
            self.group_message = False


    @classmethod
    def create_message(cls, body, message_type, group_message, user, channel_information):
        message = cls(body, message_type, group_message, user, channel_information)
        return message

    def get_as_dict(self):
        try:
            message_dict = self._create_message_dict()
            return message_dict
        except (ValueError, AttributeError) as e:
            logger.critical("Dictionary could not be created. Reason: %s", e)
            return None

    def get_sender(self):
        return self.sender

    def get_message_id(self):
        # TODO: some hashing would be nice
        return str(self._id, errors="ignore")

    def _form_message(self):
        receivers = {}
        for rc in self.receivers:
            receivers[rc] = {'sent': False, 'seen': False, 'answer': ''}

        formed_message = {
            'id': self.get_message_id(),
            'body': self.messge_body,
            'type': self.message_type,
            'group_message': self.group_message,
            'receivers': receivers,
        }
        return formed_message


