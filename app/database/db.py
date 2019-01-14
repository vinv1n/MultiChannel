import pymongo
import logging
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Mongo:
    """
    Class for handling database
    """
    def __init__(self, database_name):

        logger.critical("Initializing database")
        # FIXME change localhost to something else
        self.client = pymongo.MongoClient(host="mongo:27017")
        logger.critical(self.client)

        #Default collections
        self.user_collection = None
        self.message_collection = None

        self.database = self._create_database(database_name)
        if self.database is None:
            raise Exception("Failure in database creation")

        self._create_default_collections()
        self._create_admin()

    def _create_database(self, name):
        try:
            database = self.client[name]
            return database
        except Exception:
            return None

    def create_new_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    def get_collections(self):
        return self.database.list_collection_names()

    def _create_default_collections(self):
        self.user_collection = self.database['users']
        self.message_collection = self.database['messages']

    def _create_admin(self):
        admin_data = {
"username": "admin",
"password": pbkdf2_sha256.encrypt(saslprep("admin")),
"admin" : True,
"preferred_channel": "email",
"channels": {
            "email": {"address": "adderss@server.fi"},
            "facebook": {"user_id": "user"},
            "telegram": {"user_id": "user"},
            "irc": {"nickname": "user", "network": "user"},
            "slack": {"channel": "user","username": "user"}
           }
}
        
        cursor =  self.user_collection.find({'username': 'admin'})
        if cursor.count() == 0:
            self.user_collection.insert_one(admin_data)
            return
        else:
            return