import pymongo


class Mongo:
    """
    Class for handling database
    """
    def __init__(self, database):
        # FIXME change localhost to something else
        self.client = pymongo.MongoClient(host="localhost", port=27017)

        self.database = self._create_database(database)
        if self.database is None:
            raise Exception("Failure in database creation")


    def _create_database(self, name):
        try:
            database = self.client[name]
            return database
        except Exception:
            return None

    def create_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    def get_collections(self):
        return self.database.list_collection_names()