# Author: Jure
# Date created: 4.12.2024

from ..schemas import item_schemas as schema
from ..models.item import Item
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from bson import ObjectId as Id

async def create_item(user_id : str, storage_name : str, item : schema.ItemCreate) -> Err | str:
    """
    Create an item and associate it with a user and a specific storage.

    This function retrieves the user's collection from the database and the
    corresponding storage and adds a new item to the collection. An item with
    ``amount`` specified to zero cannot be created. An item with ``code_id``
    already existant in the database cannot be created. If the database collection
    cannot be retrieved, due to any of these reasons or the input fails validation,
    an error response is returned.

    Args:
        user_id (str): The identifier of the user creating the item.
        storage_name (str): The name of the storage where the item is being added.
        item (ItemCreate): The item details to be created, adhering to the schema.

    Returns:
        ErrorResponse | str: The error response if an error occurred or ``code_id`` otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        if item.amount == 0:
            return Err(message=f"Cannot create new item with zero instances.")

        item_model = Item(name=item.name, amount=item.amount, description=item.description)
        item_dict = item_model.model_dump(by_alias=True)
        result = await db_users.update_one(
            {"_id": Id(user_id), "storages.name": storage_name},
            {"$push": {"storages.$.content": item_dict}})

        if result.modified_count == 0:
            return Err(message=f"Creating item failed.")
        return item_model.code_id

    except Exception as e:
        return Err(message=f"Unknown  exception: {e}", code=500)

async def get_item(user_id : str, storage_name : str, item_code : str) -> Err | dict:
    """
    Retrieve an item from a user's storage by its unique code.

    This function retrieves a user from the database and attempts to find
    an item with the specified ``item_code`` in the given ``storage_name``. If the item is
    not found, or the operation fails for any reason, an error response is returned.

    Args:
        user_id (str): The identifier of the user who owns the storage.
        storage_name (str): The name of the storage where the item is located.
        item_code (str): The unique code of the item to retrieve.

    Returns:
        ErrorResponse | dict: The error response if an error occurred, or the item details as a dictionary.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        # A cleaner way of finding all matchings and a sanity check that there are unique.
        pipeline = [
            {"$match":
                {"_id": Id(user_id),
                "storages.name": storage_name,
                "storages.content.code_id": item_code}},
            {"$unwind": "$storages"},  # Deconstruct the storages array.
            {"$match": {"storages.name": storage_name}},  # Match the specific storage.
            {"$unwind": "$storages.content"},  # Deconstruct the content array.
            {"$match": { "storages.content.code_id": item_code}}, # Match the specific item.
            {"$replaceRoot": {"newRoot": "$storages.content"}}  # Replace the root document with the storage object.
        ]

        result = await db_users.aggregate(pipeline).to_list()
        if not result:
            return Err(message=f"Getting item '{item_code}' failed.")

        if len(result) > 1:
            return Err(message=f"Item '{item_code}' has more than one storage entry.")
        return result[0]

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def delete_item(user_id : str, storage_name : str, item_code : str) -> Err | str:
    """
    Delete an item from a user's storage.

    This function retrieves a user's collection from the database and removes an item
    with the specified ``item_code`` from the given ``storage_name``. If the item cannot
    be deleted, an error response is returned.

    Args:
        user_id (str): The identifier of the user who owns the storage.
        storage_name (str): The name of the storage from which the item is to be deleted.
        item_code (str): The unique code of the item to delete.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or ``code_id`` if the deletion was successful.
    """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"_id": Id(user_id), "storages.name": storage_name},
            {"$pull": {"storages.$.content": {"code_id": item_code}}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Deleting item '{item_code}' from '{storage_name}' failed.")
        return item_code

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def update_item(user_id : str, storage_name : str, item_code : str, item : schema.ItemUpdate) -> Err | str:
    """
       Update the details of an item in a user's storage.

       This function retrieves a user's collection from the database and updates the specified
       fields of an item with the given ``item_code`` in the provided ``storage_name``. If no fields
       are provided for update or the operation fails, an error response is returned.

       Args:
           user_id (str): The identifier of the user who owns the storage.
           storage_name (str): The name of the storage containing the item.
           item_code (str): The unique code of the item to update.
           item (ItemUpdate): The new details to update the item with, adhering to the schema.

       Returns:
           ErrorResponse | str: The error response if an error occurred, or ``code_id`` if the update was successful.
       """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        item_dict = item.model_dump(by_alias=True, exclude_unset=True)
        if not item_dict:
            return Err(message=f"All update values for item '{item_code}' are empty.")

        if item.amount == 0:
            return Err(message=f"Cannot create new item with zero instances.")

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
                {"item.code_id": item_code}
            ])

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating item '{item_code}' failed.")
        return item_code

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
