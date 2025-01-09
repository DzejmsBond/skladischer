# Author: Nina Mislej
# Date created: 5.12.2024

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import errors
from ..config import MONGO_URL, DATABASE_NAME, COLLECTION

client = AsyncIOMotorClient(MONGO_URL)

async def get_collection() -> AsyncIOMotorCollection | None:
    """
    Retrieve the users collection from the database.

    This function connects to the database, verifies the database and collection names,
    and returns the users collection. If the database or collection is invalid or inaccessible,
    it returns None. Values of ``MONGO_URL``, ``DATABASE_NAME`` and ``COLLECTION`` should be aquired from config.

    Returns:
        Collection | None: The users collection if successful, or None if an error occurred.
    """

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