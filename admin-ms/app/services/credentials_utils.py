# Author: Jure
# Date created: 4.12.2024

# OAuth2 authentication dependencies.
from fastapi.security import (
    OAuth2PasswordRequestForm)

from auth.token_utils import create_access_token

from ..models.credentials import Credentials
from ..models.token import Token
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err

from ..googlerpc.grpc_client import (
    create_sensor_user,
    create_storage_user,
    delete_sensor_user,
    delete_storage_user)

from bcrypt import checkpw

async def create_credentials(credentials: OAuth2PasswordRequestForm) -> Err | str:
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
            return result

        result = await create_sensor_user(credentials.username)
        if isinstance(result, Err):
            return result

        user_dict = Credentials(username=credentials.username,
                                password=credentials.password)
        result = await db_admin.insert_one(user_dict)
        if not result.acknowledged:
            return Err(message=f"Creating user failed.")

        # NOTE: We could use 'await get_user(result.inserted_id)' to get / check success.
        return credentials.username

    # TODO: Should the end user know what error happened internally?
    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def validate_credentials(credentials: OAuth2PasswordRequestForm) -> Err | Token:
    """
    Validate a user by their password and username.

    This function fetches a user's details from the database based on their credentials.
    If the user does not have existing credentials or the operation fails, an error response is returned.

    Args:
        credentials (ValidateCredentials): The password of the user to validate.

    Returns:
        ErrorResponse | Token: The error response if an error occurred, or the user's token otherwise.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        result  = await db_admin.find_one({"username": credentials.username})
        if not result or "password" not in result or "username" not in result:
            return Err(message=f"User validation '{credentials.username}' failed.", code=401)

        check = checkpw(credentials.password.encode('utf8'), result["password"].encode('utf8'))
        if not check:
            return Err(message=f"Password for '{credentials.username}' is wrong.", code=401)

        token = await create_access_token(data={"username" : credentials.username})
        return Token(access_token=token, token_type="bearer")

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_credentials(username: str) -> Err | str:
    """
    Delete a user by their identifier.

    This function removes a user from the database based on their `user_id``.
    If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or username if the deletion was successful.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        # TODO: Improve this rollback.
        result = await delete_storage_user(username)
        if isinstance(result, Err):
            return result

        result = await delete_sensor_user(username)
        if isinstance(result, Err):
            return result

        result = await db_admin.delete_one({"username": username})
        if not result.acknowledged or result.deleted_count == 0:
            return Err(message=f"Deleting user '{username}' failed.")
        return username

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def update_password(username: str, password: str) -> Err | str:
    """
    Update the password of a user.

    This function changes a user's password in the database.
    If the operation fails, an error response is returned.
    Username cannot be updated.

    Args:
        username (str): The username of the user.
        password (str): The password to be updated by the user.

    Returns:
        ErrorResponse | st: The error response if an error occurred, or username if the update was successful.
    """

    try:
        db_admin = await get_collection()
        if db_admin is None:
            return Err(message=f"Cannot get DB collection.")

        credentials = Credentials(username=username, password=password)
        result = await db_admin.update_one(
            {"username": credentials.username},
            {"$set": {"password": credentials.password}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating the password failed.")
        return username

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
