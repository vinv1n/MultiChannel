import logging
import threading
from flask import Flask
from flask_restful import Api, Resource

logger = logging.getLogger(__name__)


class Update(Resource):
    """
    For cron job to update database status from all channels
    """

    def __init__(self, handler, channels):
        self.database = handler
        self.channels = channels

    def get(self):
        thread = threading.Thread(target=self._update, kwargs={"database": self.database, "channels": self.channels})
        thread.start()
        return {"result": "ok"}, 200

    @staticmethod
    def _update(*args, **kwargs):
        database, channels = kwargs.values()

        for func in channels.items():
            result = None
            try:
                result = func()
            except Exception as e:
                logger.critical("Error during update. Error %s", e)
                continue

            if result:
                try:
                    # TODO correct function
                    database.mark_message_seen(result)
                except Exception:
                    logger.warning("Result could not be inserted to database")
                    continue
