import pymongo


class Mongo:
    """
    Class for handling database
    """
    def __init__(self, database_name):
        # FIXME change localhost to something else
        self.client = pymongo.MongoClient(host="0.0.0.0", port=27017)

        #Default collections
        self.user_collection = None
        self.message_collection = None

        self.database = self._create_database(database_name)
        if self.database is None:
            raise Exception("Failure in database creation")

        self._create_default_collections()

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
