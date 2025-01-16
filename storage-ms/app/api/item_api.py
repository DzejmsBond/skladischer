# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse

# OAuth2 authentication dependencies.
from auth.token_bearer import JWTBearer
from auth.token_utils import validate_token_with_username

# Internal dependencies.
from ..schemas import item_schemas as schema
from ..models.item import Item
from ..services import item_utils as utils
from ..helpers.error import ErrorResponse as Err

token_bearer = JWTBearer()

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{username}/{storage_name}/create-item", status_code=200, response_class=PlainTextResponse)
async def create_item(username: str, storage_name: str, item_schema: schema.ItemCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows the creation of a new item within a specific storage for a user.

    Args:
        username (str): The username of the user.
        storage_name (str): The name of the storage where the item will be created.
        item_schema (ItemCreate): The item details to be created.
        token (str): Access token generated at login time.


    Raises:
        HTTPException: If an error occurs during item creation.

    Returns:
        PlainTextResponse: The item code if the item is created successfully.
    """

    if not validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.create_item(username, storage_name, item_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}/{storage_name}/{item_code}", response_model=Item)
async def get_item(username: str, storage_name: str, item_code: str, token : str = Depends(token_bearer)):
    """
    This endpoint fetches an item by its unique code from a user's specified storage.

    Args:
        username (str): The username of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during item retrieval.

    Returns:
        Item: The retrieved item details.
    """

    if not validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.get_item(username, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}/{storage_name}/{item_code}", status_code=200, response_class=PlainTextResponse)
async def delete_item(username: str, storage_name: str, item_code: str, token : str = Depends(token_bearer)):
    """
    Delete an item from a user's storage.

    This endpoint removes an item from a specific storage by its unique code.

    Args:
        username (str): The identifier of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item to delete.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during item deletion.

    Returns:
        PlainTextResponse: The item code if the item is deleted successfully.
    """

    if not validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.delete_item(username, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/{storage_name}/{item_code}", status_code=200, response_class=PlainTextResponse)
async def update_item(username: str, storage_name: str,  item_code: str, item : schema.ItemUpdate, token : str = Depends(token_bearer)):
    """
    This endpoint allows updating the details of an existing item in a specified storage.

    Args:
        username (str): The identifier of the user.
        storage_name (str): The name of the storage containing the item.
        item_code (str): The unique code of the item to update.
        item (ItemUpdate): The updated item details.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during item update.

    Returns:
        PlainTextResponse: The item code if the item is updated successfully.
    """

    if not validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.update_item(username, storage_name, item_code, item)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result
