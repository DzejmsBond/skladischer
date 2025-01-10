# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create-user", status_code=200, response_class=PlainTextResponse)
async def create_user(user_schema : schema.UserCreate):
    """
    This endpoint allows creating a new user in the system.

    Args:
        user_schema (UserCreate): The details of the user to create.

    Raises:
        HTTPException: If an error occurs during user creation.

    Returns:
        PlainTextResponse: The user id if the user is created successfully.
    """

    result = await utils.create_user(user_schema)
    if isinstance(result, Err):
        print(f"Creating user failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    This endpoint fetches the details of a user from the system.

    Args:
        user_id (str): The identifier of the user to retrieve.

    Raises:
        HTTPException: If an error occurs during user retrieval.

    Returns:
        User: The retrieved user details.
    """

    result = await utils.get_user(user_id)
    if isinstance(result, Err):
        print(f"Getting user {user_id} failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{user_id}", status_code=200, response_class=PlainTextResponse)
async def delete_user(user_id: str):
    """
    This endpoint removes a user from the system by their identifier.

    Args:
        user_id (str): The identifier of the user to delete.

    Raises:
        HTTPException: If an error occurs during user deletion.

    Returns:
        PlainTextResponse: The user id if the user is deleted successfully.
    """

    result = await utils.delete_user(user_id)
    if isinstance(result, Err):
        print(f"Deleting user {user_id} failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{user_id}/update-name", status_code=200, response_class=PlainTextResponse)
async def update_display_name(user_id: str, new_name : str):
    """
    This endpoint allows updating the display name of a user.

    Args:
        user_id (str): The identifier of the user to update.
        new_name (str): The new display name for the user.

    Raises:
        HTTPException: If an error occurs during display name update.

    Returns:
        PlainTextResponse: The user id if the users display name is updated successfully.
    """

    result = await utils.update_display_name(user_id, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{user_id}/empty-storages", status_code=200, response_class=PlainTextResponse)
async def empty_storages(user_id: str):
    """
    This endpoint clears all storages in a user's account.

    Args:
        user_id (str): The identifier of the user whose storages will be emptied.

    Raises:
        HTTPException: If an error occurs during storages clearing.

    Returns:
        PlainTextResponse: The user id if the user storages are emptied successfully.
    """

    result = await utils.empty_storages(user_id)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result