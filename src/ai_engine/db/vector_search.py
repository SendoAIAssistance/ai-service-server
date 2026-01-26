from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time
from app.config import settings

uri = settings.MONGODB_ATLAS_URI
client = MongoClient(uri)
