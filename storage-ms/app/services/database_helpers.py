# Author: Nina Mislej
# Date created: 5.12.2024

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors

# MongoDB connection settings.
MONGO_URL = "cskladischerdb.mf4qp.mongodb.net"
DATABASE_NAME = "@skladischer-db"
COLLECTIONS = {
    "users" : "users"
}

from pymongo import MongoClient

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

def get_users_collection():
    if "users" in COLLECTIONS:
        try : return db[COLLECTIONS["users"]]
        except errors.InvalidName : return None
    return None