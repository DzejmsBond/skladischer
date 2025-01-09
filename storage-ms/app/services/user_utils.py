# Author: Jure
# Date created: 4.12.2024
from typing import Any, Mapping

from ..schemas import user_schemas as schema
from ..models.user import User
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from bson import ObjectId as Id

# TODO: What would be better than None?
#       Returning 'user' seems to be misleading because it is not really part of the result.
async def create_user(user : schema.UserCreate) -> Err | str:
    """
    Create a new user in the database.

    This function inserts a new user into the database. If the operation fails for
    any reason, an error response is returned.

    Args:
        user (UserCreate): The user details to be created, adhering to the schema.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or generated id otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        display_name = user.display_name
        user_dict = User(display_name=display_name, storages=[]).model_dump(by_alias=True)
        result = await db_users.insert_one(user_dict)
        if not result.acknowledged:
            return Err(message=f"Creating user failed.")

        # NOTE: We could use 'await get_user(result.inserted_id)' to get / check success.
        return str(result.inserted_id)

    # TODO: Should the end user know what error happened internally?
    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def get_user(user_id : str) -> Err | dict:
    """
    Retrieve a user by their identifier.

    This function fetches a user's details from the database based on their ``user_id``.
    If the user does not exist or the operation fails, an error response is returned.

    Args:
        user_id (str): The identifier of the user to retrieve.

    Returns:
        ErrorResponse | dict: The error response if an error occurred, or the user's details as a dictionary.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result: dict | None = await db_users.find_one({"_id": Id(user_id)})
        if not result:
            return Err(message=f"Getting user '{user_id}' failed.")
        return result

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_user(user_id : str) -> Err | None:
    """
    Delete a user by their identifier.

    This function removes a user from the database based on their `user_id``.
    If the operation fails, an error response is returned.

    Args:
        user_id (str): The identifier of the user to delete.

    Returns:
        ErrorResponse | None: The error response if an error occurred, or None if the deletion was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.delete_one({"_id": Id(user_id)})
        if not result.acknowledged:
            return Err(message=f"Deleting user '{user_id}' failed.")
        return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def update_display_name(user_id : str, new_name : str) -> Err | None:
    """
    Update the display name of a user.

    This function changes a user's display name in the database.
    If the operation fails, an error response is returned.

    Args:
        user_id (str): The identifier of the user whose display name is to be updated.
        new_name (str): The new display name for the user.

    Returns:
        ErrorResponse | None: The error response if an error occurred, or None if the update was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"_id": Id(user_id)},
            {"$set": {"display_name": new_name}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating display name with '{new_name}' failed.")
        return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def empty_storages(user_id : str) -> Err | None:
    """
    Empty all storages for a specific user.

    This function clears all the storage objects for a user from the database.
    If the operation fails, an error response is returned.

    Args:
        user_id (str): The identifier of the user whose storages are to be emptied.

    Returns:
        ErrorResponse | None: The error response if an error occurred, or None if the storages were successfully emptied.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"_id": Id(user_id)},
            {"$set": {"storages": []}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Emptying storages failed.")
        return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
