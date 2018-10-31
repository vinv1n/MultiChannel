class database_handler():
    """
    This is the generic formula for accessing databases.
    When new database types are added, they must follow
    the structure laid out here.
    API code expects to call a class with the following
    functions in it.
    """

    def get_users(self):
        """
        :return: list of user IDs.
        """
        pass

    def get_user(self, user_id):
        """
        Get user data.

        :param string user_id: the ID of the user.
        :return: the user data as a dictionary.
        """
        pass

    def create_user(self, user_data):
        """
        Create a new user.

        :param dict user_data: New user data.
        :return: ID of the newly created user. None if creation failed.
        """
        pass

    def update_user(self, user_info, user_id):
        """
        Update the information of a user.

        :param dict user_data: The data of the user who is being updated.
        :param string user_id: the ID of the user who is being updated.
        :return: True if update was succesful, false otherwise.
        """
        pass

    def delete_user(self, user_info):
        """
        Delete user data.

        :param string user_id: the ID of the deleted user.
        :return: True if deletion was successful, False otherwise.
        """
        pass

    def get_messages(self):
        """
        :return: list of message IDs.
        """
        pass

    def get_message(self, message_id):
        """
        Get a message from database with given ID.

        :param string message_id: the ID of the message.
        :return: the message data as a dictionary.
        """
        pass

    def create_message(self, message_data):
        """
        Create a new message.

        :param dict message_data: Dictionary of the message data.
        :return: ID of the newly created message. None if creation failed.
        """
        pass

    def delete_message(self, message_id):
        """
        Delete the messsage with given ID from database.

        :param string message_id: the ID of the message.
        :return: True if deletion successed, False otherwise.
        """
        pass

    def mark_message_seen(self, message_id, user_id):
        """
        Mark the given message seen by the user.

        Do this only if the message type is 'ack' or 'answer',
        with other types raise an error.

        :param string message_id: the ID of the seen message.
        :param string user_id: the ID of the user who has seen the message.
        :return: True if the operation was successful, False otherwise.
        """
        pass

    def add_answer_to_message(self, message_id, user_id, answer):
        """
        Add the given answer to the message by the user.

        Do this only if the message type is 'answer',
        with other types raise an error.

        :param string message_id: the ID of the answered message.
        :param string user_id: the ID of the user who answered the message.
        :return: True if the operation was successful, False otherwise.
        """
        pass
