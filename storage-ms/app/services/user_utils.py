# Author: Jure
# Date created: 4.12.2024

from typing import Any, Mapping

from ..schemas import user_schemas as schema
from ..models.user import User
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err

# logger default library.
from ..logger_setup import get_logger
logger = get_logger("storage-ms.services")

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
        ErrorResponse | str: The error response if an error occurred, or the username otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await get_user(user.username)
        if not isinstance(result, Err):
            return Err(message=f"User with username {user.username} already exists.", code=402)

        user_dict = User(username=user.username,
                         display_name=user.display_name,
                         storages=[]).model_dump(by_alias=True)
        result = await db_users.insert_one(user_dict)
        if not result.acknowledged:
            return Err(message=f"Creating user failed.")

        logger.debug(f"User '{user.username}' created.")
        return str(user.username)

    # TODO: Should the end user know what error happened internally?
    except Exception as e:
        logger.warning(f"Could not create user: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)


async def get_user(username : str) -> Err | dict:
    """
    Retrieve a user by their identifier.

    This function fetches a user's details from the database based on their ``username``.
    If the user does not exist or the operation fails, an error response is returned.

    Args:
        username (str): The identifier of the user to retrieve.

    Returns:
        ErrorResponse | dict: The error response if an error occurred, or the user's details as a dictionary.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result: dict | None = await db_users.find_one({"username": username})
        if not result:
            return Err(message=f"Getting user '{username}' failed.")
        return result

    except Exception as e:
        logger.warning(f"Could not get user: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_user(username : str) -> Err | str:
    """
    Delete a user by their identifier.

    This function removes a user from the database based on their `username``.
    If the operation fails, an error response is returned.

    Args:
        username (str): The identifier of the user to delete.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or username if the deletion was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.delete_one({"username": username})
        if not result.acknowledged:
            return Err(message=f"Deleting user '{username}' failed.")
        return username

    except Exception as e:
        logger.warning(f"Could not delete user: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)

async def update_display_name(username : str, new_name : str) -> Err | str:
    """
    Update the display name of a user.

    This function changes a user's display name in the database.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user whose display name is to be updated.
        new_name (str): The new display name for the user.

    Returns:
        ErrorResponse | st: The error response if an error occurred, or username if the update was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username},
            {"$set": {"display_name": new_name}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating display name with '{new_name}' failed.")
        return username

    except Exception as e:
        logger.warning(f"Could not update user: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)

async def empty_storages(username : str) -> Err | str:
    """
    Empty all storages for a specific user.

    This function clears all the storage objects for a user from the database.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user whose storages are to be emptied.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or username if the storages were successfully emptied.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username},
            {"$set": {"storages": []}})

        if not result.acknowledged:
            return Err(message=f"Emptying '{username}' contents failed.")

        if result.matched_count == 0:
            return Err(message=f"Couldnt match to any record in datbabase.")

        logger.debug(f"User '{username}' deleted.")
        return username

    except Exception as e:
        logger.warning(f"Could not empty user's storages: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)
