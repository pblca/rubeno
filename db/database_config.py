from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.logger import log_setup

_log = log_setup(__name__)
load_dotenv()


class Database:

    def __init__(self):
        self.col = None
        self.db = None
        self.client = None
        self.uri = None

    def setup(self):
        self.uri = os.getenv('MONGODB_STRING')
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['rubeno']
        self.col = {
            'match': self.db['matches'],
            'player': self.db['players'],
            'tournament': self.db['tournaments']
        }
        return self

    def ping(self):
        try:
            self.client.admin.command('ping')
            _log.info("Connected to MongoDB")
        except Exception as e:
            _log.error(e)
            raise e


db = Database().setup()
