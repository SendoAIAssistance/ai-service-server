from app.config import settings
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel

uri = settings.MONGODB_ATLAS_URI
client = MongoClient(uri)
