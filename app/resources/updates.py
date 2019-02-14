import logging
import threading
from flask import Flask
from flask_restful import Api, Resource

logger = logging.getLogger(__name__)


class Update(Resource):
    """
    For cron job to update database status from all channels
    Does not return anything
    """

    def __init__(self, handler, channels):
        self.database = handler
        self.channels = channels
        self.active = []

    def get(self):
        thread = threading.Thread(target=self._update, kwargs={"channels": self.channels})
        thread.start()
        return 200

    @staticmethod
    def _update(*args, **kwargs):
        channels = args[0]
        if not isinstance(channels, set):
            return None

        results = {}
        for name, func in channels.items():
            try:
                success = func.get_updates()
                if not success:
                    results.update({name: False})
                else:
                    results.update({name: True})
            except Exception as e:
                results.update({name: False})
                logger.critical("Error during update. Error %s  in %s", e, func.__class__)
                continue

            results.update({name: True})
        return results, 200
