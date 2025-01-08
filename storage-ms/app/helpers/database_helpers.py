# Author: Nina Mislej
# Date created: 5.12.2024

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from ..config import MONGO_URL, DATABASE_NAME, COLLECTION

client = AsyncIOMotorClient(MONGO_URL)

async def get_users_collection():
    names = await client.list_database_names()
    if DATABASE_NAME not in names:
        return None

    db = client[DATABASE_NAME]
    try:
        return db.get_collection(COLLECTION)
    except errors.InvalidName:
        print(f"Invalid name for collection: {COLLECTION}")
        return None
    except Exception as e:
        print(f"Unknown exception: {e}")
        return None