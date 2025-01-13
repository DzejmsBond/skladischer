# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
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
        PlainTextResponse: The username if the user is created successfully.
    """

    result = await utils.create_user(user_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}", response_model=User)
async def get_user(username: str):
    """
    This endpoint fetches the details of a user from the system.

    Args:
        username (str): The username of the user to retrieve.

    Raises:
        HTTPException: If an error occurs during user retrieval.

    Returns:
        User: The retrieved user details.
    """

    result = await utils.get_user(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}", status_code=200, response_class=PlainTextResponse)
async def delete_user(username: str):
    """
    This endpoint removes a user from the system by their username.

    Args:
        username (str): The username of the user to delete.

    Raises:
        HTTPException: If an error occurs during user deletion.

    Returns:
        PlainTextResponse: The username if the user is deleted successfully.
    """

    result = await utils.delete_user(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/update-name", status_code=200, response_class=PlainTextResponse)
async def update_display_name(username: str, new_name : str):
    """
    This endpoint allows updating the display name of a user.

    Args:
        username (str): The username of the user to update.
        new_name (str): The new display name for the user.

    Raises:
        HTTPException: If an error occurs during display name update.

    Returns:
        PlainTextResponse: The username if the users display name is updated successfully.
    """

    result = await utils.update_display_name(username, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/empty-storages", status_code=200, response_class=PlainTextResponse)
async def empty_storages(username: str):
    """
    This endpoint clears all storages in a user's account.

    Args:
        username (str): The username of the user whose storages will be emptied.

    Raises:
        HTTPException: If an error occurs during storages clearing.

    Returns:
        PlainTextResponse: The username if the user storages are emptied successfully.
    """

    result = await utils.empty_storages(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result