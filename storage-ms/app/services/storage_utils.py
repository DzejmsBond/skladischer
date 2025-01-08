# Author: Jure
# Date created: 4.12.2024

from ..schemas import storage_schemas as schema
from ..models.storage import Storage
from ..helpers.database_helpers import get_users_collection
from ..helpers.error import ErrorResponse as Err
from bson import ObjectId as Id

async def create_storage(user_id : str, storage : schema.Create):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    # NOTE: No need to check whether the user exists or not,
    # the database query does not throw but rahter returns 0 in case of no matchings.
    name = storage.name
    storage_dict = Storage(name=name, content=[]).model_dump(by_alias=True)

    if not isinstance(await get_storage(user_id, name), Err):
        return Err(message=f"Storage name '{name}' already exists and cannot be created.")

    # Update the 'user' document's field 'storages',
    # using the operator '$push' to add a value to an array.
    # Before accessing any attributes of the 'pymongo.results' objects
    # aknowledged needs to be checked:
    # if false all other attributes of this class will raise InvalidOperation when accessed.
    result = await db_users.update_one({"_id": Id(user_id)}, {"$push": {"storages": storage_dict}})
    if not result.acknowledged:
        return Err(message=f"Creating storage '{name}' failed.")

    if result.modified_count == 0:
        return Err(message=f"Creating storage '{name}' modified zero entries.")
    return None


async def get_storage(user_id : str, storage_name : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    # A cleaner way of finding all matchings and a sanity check that there are unique.
    pipeline = [
        {"$match": {"_id": Id(user_id)}}, # Finds the user.
        {"$unwind": "$storages"},  # Deconstruct the storages array.
        {"$match": {"storages.name": storage_name}}, # Match the specific storage.
        {"$replaceRoot": {"newRoot": "$storages"}}  # Replace the root document with the storage object.
    ]

    result = await db_users.aggregate(pipeline).to_list()
    if not result:
        return Err(message=f"Getting storage '{storage_name}' failed.")

    if len(result) > 1:
        return Err(message=f"Storage '{storage_name}' has more than one storage entry.")
    return result[0]


async def delete_storage(user_id : str, storage_name : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    result = await db_users.update_one(
        {"_id": Id(user_id)},
        {"$pull": {"storages": {"name": storage_name}}})

    if not result.acknowledged or result.modified_count == 0:
        return Err(message=f"Deleting storage '{storage_name}' failed.")
    return None


async def update_storage_name(user_id : str, storage_name : str, new_name : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    if not isinstance(await get_storage(user_id, new_name), Err):
        return Err(message=f"Storage name '{new_name}' already exists.")

    result = await db_users.update_one(
        {"_id": Id(user_id), "storages.name": storage_name},
        {"$set": {"storages.$.name": new_name}})

    if not result.acknowledged or result.modified_count == 0:
        return Err(message=f"Updating storage name '{storage_name}' with '{new_name}' failed.")
    return None

async def empty_storage(user_id : str, storage_name : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    result = await db_users.update_one(
        {"_id": Id(user_id), "storages.name": storage_name},
        {"$set": {"storages.$.content": []}})

    if not result.acknowledged or result.modified_count == 0:
        return Err(message=f"Emptying '{storage_name}' contents failed.")
    return None

