# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse, JSONResponse

# OAuth2 authentication dependencies.
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm)
from auth.token_utils import validate_token_with_username

# Internal dependencies.
from ..services import credentials_utils as utils
from ..helpers.error import ErrorResponse as Err
from ..models.token import Token

router = APIRouter(
    prefix="/credentials",
    tags=["credentials"]
)

# This is the endpoint for authentication.
auth_schema = OAuth2PasswordBearer(tokenUrl="login")

# NOTE: High-risk security data is not sent by GET requests, best option is POST.

@router.post("/create-credentials", status_code=200, response_class=PlainTextResponse)
async def create_credentials(credentials: OAuth2PasswordRequestForm = Depends()):
    """
    This endpoint allows creating new user credentials in the system.

    Args:
        credentials (OAuth2PasswordRequestForm): The details of the user to create.

    Raises:
        HTTPException: If an error occurs during user creation.

    Returns:
        PlainTextResponse: The username if the user is created successfully.
    """

    result = await utils.create_credentials(credentials)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/login", response_model=Token)
async def validate_credentials(credentials: OAuth2PasswordRequestForm = Depends()):
    """
    This endpoint validates the details of a user based on their username and password.

    Args:
        credentials (OAuth2PasswordRequestForm): The users credentials.

    Raises:
        HTTPException: If an error occurs during user validation.

    Returns:
        Token: The retrieved username.
    """

    result = await utils.validate_credentials(credentials)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/delete-user", status_code=200, response_class=PlainTextResponse)
async def delete_credentials(username: str, token: str = Depends(auth_schema)):
    """
    This endpoint removes a user from the system by their credentials.

    Args:
        token (OAuth2PasswordRequestForm): The users credentials.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during user deletion.

    Returns:
        PlainTextResponse: The username if the user is deleted successfully.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.delete_credentials(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/update-password", status_code=200, response_class=PlainTextResponse)
async def update_password(username: str, password: str, token: str = Depends(auth_schema)):
    """
    This endpoint allows updating the display name of a user.

    Args:
        password (OAuth2PasswordRequestForm): The credentials with new password.
        token (OAuth2PasswordRequestForm): The users credentials.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during password update.

    Returns:
        PlainTextResponse: The username if the password is updated successfully.
    """

    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.update_password(username, password)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result