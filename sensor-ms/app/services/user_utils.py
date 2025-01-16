# Author: Nina Mislej
# Date created: 13.01.2025

from typing import Any
from ..schemas import user_schemas as schema
from ..models.user import User
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from ..models.sensors import DOOR

# logger default library.
from ..logger_setup import get_logger
logger = get_logger("sensor-ms.services")

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

        logger.info(f"Created user: {user.username}")
        return str(user.username)

    except Exception as e:
        logger.warning(f"Failed creating user: {e}")
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
        logger.warning(f"Failed getting user: {e}")
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

        logger.info(f"Deleted user: {username}")
        return username

    except Exception as e:
        logger.warning(f"Failed deleting user: {e}")
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
        logger.warning(f"Failed deleting all user sensors: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)

async def get_all_door_sensors(username : str) -> Err | list:
    """
    Fetches all door sensors for a specific user.

    This function fetches a list of door sensor objects from a user's list of sensors.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the sensors.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or the list of door sensors was successfully retrieved.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        # A cleaner way of finding all matchings and a sanity check that there are unique.
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$sensors"},  # Deconstruct the sensors array.
            {"$match": {"sensors.data.type": DOOR}}, # Match all sensors of type door.
            {"$replaceRoot": {"newRoot": "$sensors"}}  # Replace the root document with the sensors object.
        ]

        result = await db_users.aggregate(pipeline).to_list()
        if not result:
            return []

        return result

    except Exception as e:
        logger.warning(f"Failed getting all door sensors: {e}")
        return Err(message=f"Unknown exception: {e}", code=500)