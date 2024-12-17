# Author: Jure
# Date created: 4.12.2024
from bson import ObjectId
from pydantic import ValidationError

from ..schemas import user_schemas as schema
from ..models.user import User
from ..models.storage import Storage
from ..models.py_object_id import PyObjectId
from .database_helpers import get_users_collection

async def create_user(user_create : schema.UserCreate):
    ref_id = user_create.ref_id
    display_name = user_create.display_name
    user = User(ref_id=ref_id, display_name=display_name, storages=[] )
    db_users = await get_users_collection()
    if db_users is None:
        return None

    user_dict = user.model_dump(by_alias=True)
    result = await db_users.insert_one(user_dict)
    if not result.acknowledged:
        return None
    return user

async def get_user(user_id : str):
    db_users = await get_users_collection()
    if db_users is None:
        return None

    result = await db_users.find_one({"_id": user_id})
    if not result:
        return None
    return result


async def create_storage(user_id : str, storage_create : schema.StorageCreate):
    db_users = await get_users_collection()
    if db_users is None:
        return None

    # Ensure user exists
    user = await db_users.find_one({"_id": user_id})
    if not user:
        return None
    name = storage_create.name
    storage = Storage(user_id=PyObjectId(user_id), name=name, content=[])
    storage_dict = storage.model_dump(by_alias=True)
    # Update the 'user' document's field 'storages', using the operator '$push' to add a value to an array.
    result = await db_users.update_one({"_id": user_id}, {"$push": {"storages": storage_dict}})

    if result.modified_count == 0:
        print("Unable to modify user")
        return None
    return storage


async def get_storage(storage_id : str):
    return None

async def update_storage(storage_update : schema.StorageUpdate):
    return None

async def delete_storage(storage_delete : schema.StorageDelete):
    return None