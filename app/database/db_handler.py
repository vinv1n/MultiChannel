import logging

from app.database.db import Mongo
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)


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
        :return: list of users and their data.
        """
        try:
            envelope = []
            cursor = self.database.user_collection.find({ })

            for item in cursor:
                user = {}
                for key in item:
                    if key == "password":
                        pass
                    elif key == "_id":
                        user[key] = str(item[key])
                    else:
                        user[key] = item[key]
                envelope.append(user)

            return envelope
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def get_user(self,user_id):
        """
        Get user data.

        :param string user_id: the ID of the user.
        :return: the user data as a dictionary.
        """

        try:
            cursor = self.database.user_collection.find({'_id': ObjectId(user_id)})

            if cursor.count() == 0:
                return None

            for item in cursor:
                user = {}
                for key in item:
                    if key == "password":
                        pass
                    elif key == "_id":
                        user[key] = str(item[key])
                    else:
                        user[key] = item[key]
                break

            return user
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def get_user_name(self, username):
        """
        Get user data.

        :param string username: the username of the user.
        :return: the user data as a dictionary.
        """
        try:
            cursor = self.database.user_collection.find({'username': username})

            if cursor.count() == 0:
                return None

            for item in cursor:
                user = {}
                for key in item:
                    if key == "_id":
                        user[key] = str(item[key])
                    else:
                        user[key] = item[key]
                break

            return user
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def create_user(self, user_data):
        """
        Create a new user.

        :param dict user_data: New user data.
        :return: ID of the newly created user. None if creation failed.
        """
        check = self.database.user_collection.find({"username": user_data["username"]})
        if check.count() > 0:
            return "used"
        try:
            result = self.database.user_collection.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def update_user(self, user_info, user_id):
        """
        Update the information of a user.

        :param dict user_data: The data of the user who is being updated.
        :param string user_id: the ID of the user who is being updated.
        :return: True if update was succesful, false otherwise.
        """
        # acknowledged returns True if document is modified, otherwise false

        try:
            result = self.database.user_collection.update(
                {"_id": ObjectId(user_id)},
                {"$set": user_info}
                )
            if result["nModified"] > 0:
                return 200
            else:
                return 304
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def delete_user(self, user_id):
        """
        Delete user data.

        :param string user_id: the ID of the deleted user.
        :return: True if deletion was successful, False otherwise.
        """
        try:
            result = self.database.user_collection.delete_one(filter={'_id': ObjectId(user_id)}).acknowledged
            return result
        except Exception as e:
            logger.critical("Error during data handling: %s", e)
            return None

    def get_messages(self):
        """
        :return: list of message IDs.
        """
        try:
            data = self.database.message_collection.find({})
            envelope = []
            for item in data:
                message = {}
                for key in item:
                    if key == "_id":
                        message.update({key: str(item[key])})
                    else:
                        message.update({key: item[key]})
                envelope.append(message)
            return envelope
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None
    
    def get_message(self, message_id):
        
        """Get a message from database with given ID.

        :param string message_id: the ID of the message.
        :return: the message data as a dictionary."""

        try:
            cursor = self.database.message_collection.find({'_id': ObjectId(message_id)})
            message = {}
            for item in cursor:
                for key in item:
                    if key == "_id":
                        message.update({key: str(item[key])})
                    else:
                        message.update({key: item[key]})
            return message
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def create_message(self, message_data):
        """
        Create a new message.

        :param dict message_data: Dictionary of the message data.
        :return: ID of the newly created message. None if creation failed.
        """
        try:
            result = self.database.message_collection.insert_one(message_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def delete_message(self, message_id):
        """
        Delete the messsage with given ID from database.

        :param string message_id: the ID of the message.
        :return: True if deletion successed, False otherwise.
        """
        try:
            result = self.database.message_collection.delete_one(filter={'_id': ObjectId(message_id)}).acknowledged
            return result
        except Exception as e:
            logger.critical("Error during data handling. Error: %s", e)
            return None

    def mark_message_seen(self, message_id, user_id):
        """
        Mark the given message seen by the user.
        :param string message_id: Message ID which has been seen by the user.
        :param string user_ids: the ID of the user who has seen the message.
        :return: True if the operation was successful, False otherwise.
        Message sctructure
        message = {
            "_id": id,
            "content": str,
            "sender": str,
            "timestamp": timestamp
            "receivers": {
                user_id: {
                    "seen": bool,
                    "sent": bool,
                    "answer": str
                }
            }
        }
        """

        message = self.get_message(message_id)
        if not message:
            raise ValueError('Could not find message with id: {}'.format(message_id))
        receivers_as_dict = message.get("receivers")
        if not receivers_as_dict:
            raise ValueError("Message does not have receivers")

        user_status = receivers_as_dict.get(user_id)
        if not user_status:
            raise ValueError('Could not find user: {}'.format(user_id))
        user_status['seen'] = True

        result = self.database.message_collection.update(
            {"_id": ObjectId(message_id)},
            {"$set": {"receivers": receivers_as_dict}}
        )

        if result["nModified"] > 0:
            return True
        else:
            return False

    def add_answer_to_message(self, message_id, user_id, answer):
        """
        Add the given answer to the message by the user.
        Do this only if the message type is 'answer',
        with other types raise an error.
        :param string message_id: the ID of the answered message.
        :param string user_id: the ID of the user who answered the message.
        :return: True if the operation was successful, False otherwise.
        """
        message = self.get_message(message_id)
        if not message:
            raise ValueError('Could not find message with id: {}'.format(message_id))
        receivers_as_dict = message.get("receivers")
        if not receivers_as_dict:
            raise ValueError("Message does not have receivers")

        user_status = receivers_as_dict.get(user_id)
        if not user_status:
            raise ValueError('Could not find user: {}'.format(user_id))
        user_status['seen'] = True
        user_status['answer'] = answer

        result = self.database.message_collection.update(
            {"_id": ObjectId(message_id)},
            {"$set": {"receivers": receivers_as_dict}}
        )

        if result["nModified"] > 0:
            return True
        else:
            return False

    def set_message_sent(self, message_id, user_ids):
        """
        :param string message_id: the ID of the message.
        :param list user_ids: the users who the message was sent to.
        :return: list of all IDs who the operation was succesful with.
        """
        message = self.get_message(message_id)
        if not message:
            raise ValueError('Could not find message with id: {}'.format(message_id))
        receivers_as_dict = message.get("receivers")
        if not receivers_as_dict:
            raise ValueError("Message does not have receivers")

        successes = list()
        for user_id in user_ids:
            user_status = receivers_as_dict.get(user_id)
            if not user_status:
                logger.warning('set_message_sent: Could not find user: {}'.format(user_id))
                continue
            user_status['sent'] = True
            successes.append(user_id)

        result = self.database.message_collection.update(
            {"_id": ObjectId(message_id)},
            {"$set": {"receivers": receivers_as_dict}}
        )

        if result["nModified"] > 0:
            return successes
        else:
            return False
