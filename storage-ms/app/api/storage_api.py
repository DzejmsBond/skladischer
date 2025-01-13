# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..schemas import storage_schemas as schema
from ..services import storage_utils as utils
from ..models.storage import Storage
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{username}/create-storage", status_code=200, response_class=PlainTextResponse)
async def create_storage(username: str, storage_schema : schema.StorageCreate):
    """
    This endpoint allows the creation of a storage in a user's account.

    Args:
        username (str): The username of the user.
        storage_schema (StorageCreate): The storage details to create.

    Raises:
        HTTPException: If an error occurs during storage creation.

    Returns:
        PlainTextResponse: The storage name if the storage is created successfully.
    """

    result = await utils.create_storage(username, storage_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}/{storage_name}", response_model=Storage)
async def get_storage(username: str, storage_name: str):
    """
    This endpoint fetches the details of a specific storage for a user.

    Args:
        username (str): The username of the user.
        storage_name (str): The name of the storage to retrieve.

    Raises:
        HTTPException: If an error occurs during storage retrieval.

    Returns:
        Storage: The retrieved storage details.
    """

    result = await utils.get_storage(username, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}/{storage_name}", status_code=200, response_class=PlainTextResponse)
async def delete_storage(username: str, storage_name: str):
    """
    This endpoint removes a storage from a user's account by its name.

    Args:
        username (str): The username of the user.
        storage_name (str): The name of the storage to delete.

    Raises:
        HTTPException: If an error occurs during storage deletion.

    Returns:
        PlainTextResponse: The storage name if the storage is deleted successfully.
    """

    result = await utils.delete_storage(username, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/{storage_name}/update-name", status_code=200, response_class=PlainTextResponse)
async def update_storage_name(username: str, storage_name: str, new_name : str):
    """
    This endpoint allows renaming an existing storage in a user's account.

    Args:
        username (str): The username of the user.
        storage_name (str): The current name of the storage.
        new_name (str): The new name for the storage.

    Raises:
        HTTPException: If an error occurs during storage name update.

    Returns:
        PlainTextResponse: The storage name if the storage name is updated successfully.
    """

    result = await utils.update_storage_name(username, storage_name, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/{storage_name}/empty-storage", status_code=200, response_class=PlainTextResponse)
async def empty_storage(username: str, storage_name: str):
    """
    This endpoint clears all items from a specified storage.

    Args:
        username (str): The username of the user.
        storage_name (str): The name of the storage to empty.

    Raises:
        HTTPException: If an error occurs during storage clearing.

    Returns:
        PlainTextResponse: The storage name if the storage is emptied successfully.
    """

    result = await utils.empty_storage(username, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result