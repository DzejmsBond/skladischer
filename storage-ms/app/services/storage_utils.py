# Author: Jure
# Date created: 4.12.2024

from ..schemas import storage_schemas as schema
from ..models.storage import Storage
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err

async def create_storage(username : str, storage : schema.StorageCreate) -> Err | str:
    """
    Create a new storage for a specific user.

    This function adds a new storage to the user's storage list. If a storage with the
    same name already exists, or if the operation fails for any reason, an error response
    is returned.

    Args:
        username (str): The username of the user creating the storage.
        storage (StorageCreate): The storage details to be created, adhering to the schema.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or storage name otherwise.
    """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        # NOTE: No need to check whether the user exists or not,
        # the database query does not throw but rahter returns 0 in case of no matchings.
        name = storage.name
        storage_dict = Storage(name=name,
                               content=[]).model_dump(by_alias=True)

        if not isinstance(await get_storage(username, name), Err):
            return Err(message=f"Storage name '{name}' already exists and cannot be created.", code=409)

        # Update the 'user' document's field 'storages',
        # using the operator '$push' to add a value to an array.
        # Before accessing any attributes of the 'pymongo.results' objects
        # aknowledged needs to be checked:
        # if false all other attributes of this class will raise InvalidOperation when accessed.
        result = await db_users.update_one({"username": username}, {"$push": {"storages": storage_dict}})
        if not result.acknowledged:
            return Err(message=f"Creating storage '{name}' failed.")

        if result.modified_count == 0:
            return Err(message=f"Creating storage '{name}' modified zero entries.")

        logging.debug(f"New storage '{name}' created.")
        return name

    except Exception as e:
        logging.warning(f"Could not create storage: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)


async def get_storage(username : str, storage_name : str) -> Err | dict:
    """
       Retrieve a storage by its name for a specific user.

       This function fetches a storage object for a user based on the `storage_name`.
       If the storage does not exist or the operation fails, an error response is returned.

       Args:
           username (str): The username of the user who owns the storage.
           storage_name (str): The name of the storage to retrieve.

       Returns:
           ErrorResponse | dict: The error response if an error occurred, or the storage details as a dictionary.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        # A cleaner way of finding all matchings and a sanity check that there are unique.
        pipeline = [
            {"$match": {"username": username}}, # Finds the user.
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

    except Exception as e:
        logging.warning(f"Could not get storage: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_storage(username : str, storage_name : str) -> Err | str:
    """
    Delete a storage by its name for a specific user.

    This function removes a storage object from a user's list of storages based
    on the `storage_name`. If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the storage.
        storage_name (str): The name of the storage to delete.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or storage name if the deletion was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username},
            {"$pull": {"storages": {"name": storage_name}}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Deleting storage '{storage_name}' failed.")
        return storage_name

    except Exception as e:
        logging.warning(f"Could not delete storage: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)


async def update_storage_name(username : str, storage_name : str, new_name : str) -> Err | str:
    """
    Update the name of a storage for a specific user.

    This function changes the name of a storage in a user's storage list.
    If the new name already exists or the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the storage.
        storage_name (str): The current name of the storage to update.
        new_name (str): The new name for the storage.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or storage name if the update was successful.
    """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        if not isinstance(await get_storage(username, new_name), Err):
            return Err(message=f"Storage name '{new_name}' already exists.", code=409)

        result = await db_users.update_one(
            {"username": username, "storages.name": storage_name},
            {"$set": {"storages.$.name": new_name}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating storage name '{storage_name}' with '{new_name}' failed.")
        return new_name

    except Exception as e:
        logging.warning(f"Could not update storage: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)

async def empty_storage(username : str, storage_name : str) -> Err | str:
    """
    Empty the contents of a storage for a specific user.

    This function clears all the items in the specified storage for a user.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the storage.
        storage_name (str): The name of the storage to empty.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or storage name if the storage was successfully emptied.
    """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username, "storages.name": storage_name},
            {"$set": {"storages.$.content": []}})

        if not result.acknowledged:
            return Err(message=f"Emptying '{storage_name}' contents failed.")

        if result.matched_count == 0:
            return Err(message=f"Couldnt match to any record in datbabase.")

        logging.debug(f"Deleted storage '{storage_name}'.")
        return storage_name

    except Exception as e:
        logging.warning(f"Could not empty storage: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)

