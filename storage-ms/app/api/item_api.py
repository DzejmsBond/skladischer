# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import item_schemas as schema
from ..models.item import Item
from ..services import item_utils as utils
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{user_id}/{storage_name}/create-item", status_code=204)
async def create_item(user_id: str, storage_name: str, item_schema: schema.ItemCreate):
    """
    This endpoint allows the creation of a new item within a specific storage for a user.

    Args:
        user_id (str): The identifier of the user.
        storage_name (str): The name of the storage where the item will be created.
        item_schema (ItemCreate): The item details to be created.

    Raises:
        HTTPException: If an error occurs during item creation.

    Returns:
        dict: A success message if the item is created successfully.
    """

    result = await utils.create_item(user_id, storage_name, item_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": "Item successfully created."}

@router.get("/{user_id}/{storage_name}/{item_code}", response_model=Item)
async def get_item(user_id: str, storage_name: str, item_code: str):
    """
    This endpoint fetches an item by its unique code from a user's specified storage.

    Args:
        user_id (str): The identifier of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item.

    Raises:
        HTTPException: If an error occurs during item retrieval.

    Returns:
        Item: The retrieved item details.
    """

    result = await utils.get_item(user_id, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{user_id}/{storage_name}/{item_code}", status_code=204)
async def delete_item(user_id: str, storage_name: str, item_code: str):
    """
    Delete an item from a user's storage.

    This endpoint removes an item from a specific storage by its unique code.

    Args:
        user_id (str): The identifier of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item to delete.

    Raises:
        HTTPException: If an error occurs during item deletion.

    Returns:
        dict: A success message if the item is deleted successfully.
    """

    result = await utils.delete_item(user_id, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Item '{item_code}' successfully deleted."}

@router.put("/{user_id}/{storage_name}/update-item", status_code=204)
async def update_item(user_id: str, storage_name: str,  item_code: str, item : schema.ItemUpdate):
    """
    This endpoint allows updating the details of an existing item in a specified storage.

    Args:
        user_id (str): The identifier of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item to update.
        item (ItemUpdate): The updated item details.

    Raises:
        HTTPException: If an error occurs during item update.

    Returns:
        dict: A success message if the item is updated successfully.
    """

    result = await utils.update_item(user_id, storage_name, item_code, item)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Item '{item_code}' successfully updated."}