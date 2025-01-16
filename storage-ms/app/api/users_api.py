# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse

# OAuth2 authentication dependencies.
from skladischer_auth.token_bearer import JWTBearer
from skladischer_auth.token_utils import validate_token_with_username

# Internal dependencies.
from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User
from ..helpers.error import ErrorResponse as Err

token_bearer = JWTBearer()

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create-user", status_code=200, response_class=PlainTextResponse)
async def create_user(user_schema : schema.UserCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows creating a new user in the system.

    Args:
        user_schema (UserCreate): The details of the user to create.
        token (str): Access token generated at login time.

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
async def get_user(username: str, token : str = Depends(token_bearer)):
    """
    This endpoint fetches the details of a user from the system.

    Args:
        username (str): The username of the user to retrieve.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during user retrieval.

    Returns:
        User: The retrieved user details.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.get_user(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}", status_code=200, response_class=PlainTextResponse)
async def delete_user(username: str, token : str = Depends(token_bearer)):
    """
    This endpoint removes a user from the system by their username.

    Args:
        username (str): The username of the user to delete.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during user deletion.

    Returns:
        PlainTextResponse: The username if the user is deleted successfully.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.delete_user(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/update-name", status_code=200, response_class=PlainTextResponse)
async def update_display_name(username: str, new_name : str, token : str = Depends(token_bearer)):
    """
    This endpoint allows updating the display name of a user.

    Args:
        username (str): The username of the user to update.
        new_name (str): The new display name for the user.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during display name update.

    Returns:
        PlainTextResponse: The username if the users display name is updated successfully.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.update_display_name(username, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/empty-storages", status_code=200, response_class=PlainTextResponse)
async def empty_storages(username: str, token : str = Depends(token_bearer)):
    """
    This endpoint clears all storages in a user's account.

    Args:
        username (str): The username of the user whose storages will be emptied.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during storages clearing.

    Returns:
        PlainTextResponse: The username if the user storages are emptied successfully.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.empty_storages(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result