from pymongo import MongoClient
from app.db.config import MONGODB_URL

client = MongoClient(MONGODB_URL)

mongo_db = client["liveRatesDB"]

rates_collection = mongo_db["rates"]
