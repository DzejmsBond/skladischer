# Author: Jure
# Date created: 4.12.2024

from ..schemas import item_schemas as schema
from ..models.item import Item
from ..helpers.database_helpers import get_users_collection
from ..helpers.error import ErrorResponse as Err
from bson import ObjectId as Id

"""
User class to represent a user in the system.

:param user_id: The name of the user.
:type user_id: str
"""
async def create_item(user_id : str, storage_name : str, item : schema.ItemCreate):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    if item.amount == 0:
        return Err(message=f"Cannot create new item with zero instances.")

    item_dict = Item(name=item.name, amount=item.amount, description=item.description).model_dump(by_alias=True)
    result = await db_users.update_one(
        {"_id": Id(user_id), "storages.name": storage_name},
        {"$push": {"storages.$.content": item_dict}})

    if result.modified_count == 0:
        return Err(message=f"Creating item failed.")
    return None

async def get_item(user_id : str, storage_name : str, item_code : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    # A cleaner way of finding all matchings and a sanity check that there are unique.
    pipeline = [
        {"$match":
            {"_id": Id(user_id),
            "storages.name": storage_name,
            "storages.content.code_gen_token": item_code}},
        {"$unwind": "$storages"},  # Deconstruct the storages array.
        {"$match": {"storages.name": storage_name}},  # Match the specific storage.
        {"$unwind": "$storages.content"},  # Deconstruct the content array.
        {"$match": { "storages.content.code_gen_token": item_code}}, # Match the specific item.
        {"$replaceRoot": {"newRoot": "$storages.content"}}  # Replace the root document with the storage object.
    ]

    result = await db_users.aggregate(pipeline).to_list()
    if not result:
        return Err(message=f"Getting item '{item_code}' failed.")

    if len(result) > 1:
        return Err(message=f"Item '{item_code}' has more than one storage entry.")
    return result[0]

async def delete_item(user_id : str, storage_name : str, item_code : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    result = await db_users.update_one(
        {"_id": Id(user_id), "storages.name": storage_name},
        {"$pull": {"storages.$.content": {"code_gen_token": item_code}}})

    if not result.acknowledged or result.modified_count == 0:
        return Err(message=f"Deleting item '{item_code}' from '{storage_name}' failed.")
    return None

async def update_item(user_id : str, storage_name : str, item_code : str, item : schema.ItemUpdate):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    item_dict = item.model_dump(by_alias=True, exclude_unset=True)
    if not item_dict:
        return Err(message=f"All update values for item '{item_code}' are empty.")

    # Loop through fields and construct the update operation for the content array.
    fields_to_update = {
        f"storages.$[storage].content.$[item].{field}": value
        for field, value in item_dict.items()}

    # NOTE: This the way to loop through multiple positional arguments.
    # You cannot use multiple '$' such arguments, 'array_filters' is the correct way.
    result = await db_users.update_one(
        {"_id": Id(user_id)},
        {"$set": fields_to_update},
        array_filters = [
            {"storage.name": storage_name},
            {"item.code_gen_token": item_code}
        ])

    if not result.acknowledged or result.modified_count == 0:
        return Err(message=f"Updating item '{item_code}' failed.")
    return None