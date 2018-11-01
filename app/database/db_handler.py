from db import Mongo
import json


class database_handler:
    """
    This is the generic formula for accessing databases.
    When new database types are added, they must follow
    the structure laid out here.
    API code expects to call a class with the following
    functions in it.
    """

    def __init__(self, name=None):
        if name:
            self.database = Mongo(name)
        else:
            self.database = Mongo("multichannel")

    def get_users(self):
        """
        :return: list of user IDs.
        """
        return self.database.user_collection.distinct()

    def get_user(self, user_id):
        """
        Get user data.

        :param string user_id: the ID of the user.
        :return: the user data as a dictionary.
        """
        return self.database.user_collection.find_one(filter={'_id': user_id})

    def create_user(self, user_data):
        """
        Create a new user.

        :param dict user_data: New user data.
        :return: ID of the newly created user. None if creation failed.
        """
        try:
            id_ = self.database.user_collection.insert_one(user_data).inserted_id
            return id_
        except Exception:
            return None

    def update_user(self, user_info, user_id):
        """
        Update the information of a user.

        :param dict user_data: The data of the user who is being updated.
        :param string user_id: the ID of the user who is being updated.
        :return: True if update was succesful, false otherwise.
        """
        # acknowledged returns True if document is modified, otherwise false
        return self.database.user_collection.update_one(filter={"_id": user_id}, update=user_info).acknowledged

    def delete_user(self, user_id):
        """
        Delete user data.

        :param string user_id: the ID of the deleted user.
        :return: True if deletion was successful, False otherwise.
        """
        return self.database.user_collection.delete_one(filter={'_id': user_id}).acknowledged

    def get_messages(self):
        """
        :return: list of message IDs.
        """
        return self.database.message_collection.distinct()

    def get_message(self, message_id):
        """
        Get a message from database with given ID.

        :param string message_id: the ID of the message.
        :return: the message data as a dictionary.
        """
        return self.database.message_collection.find_one(filter={"_id": message_id})

    def create_message(self, message_data):
        """
        Create a new message.

        :param dict message_data: Dictionary of the message data.
        :return: ID of the newly created message. None if creation failed.
        """
        return self.database.message_collection.insert_one(message_data).inserted_id

    def delete_message(self, message_id):
        """
        Delete the messsage with given ID from database.

        :param string message_id: the ID of the message.
        :return: True if deletion successed, False otherwise.
        """
        return self.database.message_collection.delete_one(filter={'_id': message_id}).acknowledged

    def mark_message_seen(self, message_id, user_id):
        """
        Mark the given message seen by the user.

        Do this only if the message type is 'ack' or 'answer',
        with other types raise an error.

        :param string message_id: the ID of the seen message.
        :param string user_id: the ID of the user who has seen the message.
        :return: True if the operation was successful, False otherwise.
        """
        """
        Message sctructure?
        message = {
            "_id": id,
            "content": str,
            "sender": str,
            "sent_to": {
                user_id: {
                    "seen": bool,
                    "answer": str
                }
            }
        }

        """
        # needs to be decided if user has messages or message have users
        message = self.database.message_collection.find_one(filter={'_id': message_id})

        # these could be combined into one
        # this might bork epicly
        users_as_dict = message.get("sent_to", "")
        if not users_as_dict:
            raise ValueError("Message does not have users")  # better message

        user_status = users_as_dict.get(user_id, None)
        if not user_status:
            raise Exception("No such user")

        user_status['seen'] = True
        return self.database.message_collection.update_one(filter={"_id": message_id}, update=message).acknowledged

    def add_answer_to_message(self, message_id, user_id, answer):
        """
        Add the given answer to the message by the user.

        Do this only if the message type is 'answer',
        with other types raise an error.

        :param string message_id: the ID of the answered message.
        :param string user_id: the ID of the user who answered the message.
        :return: True if the operation was successful, False otherwise.
        """
        # needs to be decided if user has messages or message have users
        message = self.database.message_collection.find_one(filter={'_id': message_id})

        users_as_dict = message.get("sent_to", "")
        if not users_as_dict:
            raise ValueError("Message does not have users")  # better message

        user_status = users_as_dict.get(user_id, None)
        if not user_status:
            raise Exception("No such user")

        user_status['answer'] = answer
        user_status['seen'] = True

        return self.database.message_collection.update_one(filter={"_id": message_id}, update=message).acknowledged
