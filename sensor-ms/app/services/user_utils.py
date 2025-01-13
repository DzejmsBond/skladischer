# Author: Nina Mislej
# Date created: 13.01.2025

from typing import Any
from ..schemas import user_schemas as schema
from ..models.user import User
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err

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
                         sensors=[]).model_dump(by_alias=True)
        result = await db_users.insert_one(user_dict)
        if not result.acknowledged:
            return Err(message=f"Creating user failed.")

        # NOTE: We could use the following code to retrieve ID of the new record.
        # CODE: await get_user(result.inserted_id).
        return str(user.username)

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def get_user(username : str) -> Err | dict:
    """
    Retrieve a user by their username.

    This function fetches a user's details from the database based on their ``username``.
    If the user does not exist or the operation fails, an error response is returned.

    Args:
        username (str): The username of the user to retrieve.

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
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_user(username : str) -> Err | str:
    """
    Delete a user by their username.

    This function removes a user from the database based on their `username``.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user to delete.

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
        return Err(message=f"Unknown exception: {e}", code=500)

async def delete_sensors(username : str) -> Err | str:
    """
    Remove all sensors for a specific user.

    This function clears all the sensor objects for a user from the database.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user whose sensors are to be removed.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or username if the sensors were successfully removed.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username},
            {"$set": {"sensors": []}})

        if not result.acknowledged:
            return Err(message=f"Emptying '{username}' contents failed.")

        if result.matched_count == 0:
            return Err(message=f"Couldnt match to any record in datbabase.")
        return username

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
