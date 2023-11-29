import os
from pymongo import MongoClient


def init_collection():
    try:
        client = MongoClient(
            os.environ.get("MONGODB_URI") or "mongodb://localhost:27017"
        )
        db = client["weather_requests"]
        collection = db["requests"]
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
