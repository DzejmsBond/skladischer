# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..schemas import credentials_schemas as schema
from ..services import credentials_utils as utils
from ..models.credentials import Credentials
from ..helpers.error import ErrorResponse as Err
from ..models.token import Token

router = APIRouter(
    prefix="/credentials",
    tags=["credentials"]
)

# NOTE: High-risk security data is not sent by GET requests, best option is POST.

@router.post("/create-credentials", status_code=200, response_class=PlainTextResponse)
async def create_credentials(credentials_schema : schema.CreateCredentials):
    """
    This endpoint allows creating new user credentials in the system.

    Args:
        credentials_schema (CreateCredentials): The details of the user to create.

    Raises:
        HTTPException: If an error occurs during user creation.

    Returns:
        PlainTextResponse: The username if the user is created successfully.
    """

    result = await utils.create_credentials(credentials_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}", response_model=Token)
async def validate_credentials(username: str, credentials_schema : schema.ValidateCredentials):
    """
    This endpoint validates the details of a user based on their username and password.

    Args:
        credentials_schema (ValidateCredentials): The users credentials.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during user validation.

    Returns:
        Token: The retrieved username.
    """

    result = await utils.validate_credentials(username, credentials_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}", status_code=200, response_class=PlainTextResponse)
async def delete_credentials(username: str, credentials_schema : schema.ValidateCredentials):
    """
    This endpoint removes a user from the system by their credentials.

    Args:
        credentials_schema (ValidateCredentials): The users credentials.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during user deletion.

    Returns:
        PlainTextResponse: The username if the user is deleted successfully.
    """

    result = await utils.delete_credentials(username, credentials_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/update-password", status_code=200, response_class=PlainTextResponse)
async def update_password(username: str, credentials_schema : schema.UpdateCredentials):
    """
    This endpoint allows updating the display name of a user.

    Args:
        credentials_schema (UpdateCredentials): The credentials with new and old password.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during password update.

    Returns:
        PlainTextResponse: The username if the password is updated successfully.
    """

    result = await utils.update_password(username, credentials_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result