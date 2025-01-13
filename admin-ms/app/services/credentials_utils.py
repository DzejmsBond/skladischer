# Author: Jure
# Date created: 4.12.2024
from typing import Any, Mapping

from ..schemas import credentials_schemas as schema
from ..models.credentials import Credentials
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from ..googlerpc.grpc_client import (
    create_sensor_user,
    create_storage_user,
    delete_sensor_user,
    delete_storage_user)
from bcrypt import checkpw

async def create_credentials(credentials : schema.CreateCredentials) -> Err | str:
    """
    Create a new user in the database.

    This function inserts a new user credentials into the database. If the operation fails for
    any reason, an error response is returned.

    Args:
        credentials (CreateCredentials): The user credentials to be created, adhering to the schema.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or generated id otherwise.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_admin.find_one({"username": credentials.username})
        if result:
            return Err(message=f"User with username {credentials.username} already exists.")

        # TODO: Improve this rollback.
        result = await create_storage_user(credentials.username)
        if isinstance(result, Err):
            await delete_storage_user(credentials.username)
            await delete_sensor_user(credentials.username)
            return result

        if result != credentials.username:
            await delete_storage_user(result)
            await delete_sensor_user(result)
            return Err(message=f"Storage and Login username missmatch.")

        result = await create_sensor_user(credentials.username)
        if isinstance(result, Err):
            await delete_storage_user(credentials.username)
            await delete_sensor_user(credentials.username)
            return result

        if result != credentials.username:
            await delete_storage_user(result)
            await delete_sensor_user(result)
            return Err(message=f"Sensor and Login username missmatch.")

        user_dict = Credentials(username=credentials.username,
                                password=credentials.password).model_dump(by_alias=True)
        result = await db_admin.insert_one(user_dict)
        if not result.acknowledged:
            return Err(message=f"Creating user failed.")

        # NOTE: We could use 'await get_user(result.inserted_id)' to get / check success.
        return credentials.username

    # TODO: Should the end user know what error happened internally?
    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def validate_credentials(username: str, credentials : schema.ValidateCredentials) -> Err | str:
    """
    Validate a user by their password and username.

    This function fetches a user's details from the database based on their credentials.
    If the user does not have existing credentials or the operation fails, an error response is returned.

    Args:
        credentials (ValidateCredentials): The password of the user to validate.
        username (str): The user's username.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or the user's username otherwise.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        result  = await db_admin.find_one({"username": username})
        if not result or "password" not in result or "username" not in result:
            return Err(message=f"User validation '{username}' failed.", code=403)

        check = checkpw(credentials.password.encode('utf8'), result["password"].encode('utf8'))
        if not check:
            return Err(message=f"Password for '{username}' is wrong.", code=403)
        return result["username"]

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_credentials(username: str, credentials : schema.ValidateCredentials) -> Err | str:
    """
    Delete a user by their identifier.

    This function removes a user from the database based on their `user_id``.
    If the operation fails, an error response is returned.

    Args:
        credentials (ValidateCredentials): The password of the user to delete.
        username (str): The user's username.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or username if the deletion was successful.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        check = await validate_credentials(username, credentials)
        if isinstance(check, Err):
            return check

        # TODO: Improve this rollback.
        result = await delete_storage_user(username)
        if isinstance(result, Err):
            await create_storage_user(credentials.username)
            await create_sensor_user(credentials.username)
            return result

        if result != username:
            await create_storage_user(result)
            await create_sensor_user(result)
            return Err(message=f"Storage and Login username missmatch.")

        result = await delete_sensor_user(username)
        if isinstance(result, Err):
            await create_storage_user(credentials.username)
            await create_sensor_user(credentials.username)
            return result

        if result != username:
            await create_storage_user(result)
            await create_sensor_user(result)
            return Err(message=f"Sensor and Login username missmatch.")

        result = await db_admin.delete_one({"username": username})
        if not result.acknowledged or result.deleted_count == 0:
            return Err(message=f"Deleting user '{user_id}' failed.")
        return username

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def update_password(username: str, credentials: schema.UpdateCredentials) -> Err | str:
    """
    Update the password of a user.

    This function changes a user's password in the database.
    If the operation fails, an error response is returned.
    Username cannot be updated.

    Args:
        credentials (UpdateCredentials): The old and new passwords of the user.
        username (str): The user's username.

    Returns:
        ErrorResponse | st: The error response if an error occurred, or username if the update was successful.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        check = await validate_credentials(username, schema.ValidateCredentials(password=credentials.password))
        if isinstance(check, Err):
            return check

        result = await db_admin.update_one(
            {"username": username},
            {"$set": {"password": credentials.new_password}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating the password failed.")
        return username

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
