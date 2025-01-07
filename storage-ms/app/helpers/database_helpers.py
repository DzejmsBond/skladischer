# Author: Nina Mislej
# Date created: 5.12.2024
from sys import exception

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors

# MongoDB connection settings.
MONGO_URL = "mongodb+srv://admin:qg0B3fJqlwzWEy0K@skladischerdb.mf4qp.mongodb.net/?retryWrites=true&w=majority&appName=skladischerDB"
DATABASE_NAME = "skladischer"
COLLECTIONS = {
    "users" : "users"
}

client = AsyncIOMotorClient(MONGO_URL)

async def get_users_collection():
    names = await client.list_database_names()
    if DATABASE_NAME not in names:
        return None

    if "users" not in COLLECTIONS:
        return None

    db = client[DATABASE_NAME]
    collection_name = COLLECTIONS["users"]
    try:
        return db.get_collection(collection_name)
    except errors.InvalidName:
        print(f"Invalid name for collection: {collection_name}")
        return None
    except Exception as e:
        print(f"Unknown exception: {e}")
        return None