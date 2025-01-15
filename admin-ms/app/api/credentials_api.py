# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends, Path, Form
from fastapi.responses import PlainTextResponse

# OAuth2 authentication dependencies.
from typing import Annotated
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm)

# Internal dependencies.
from ..services import credentials_utils as utils
from ..models.credentials import Credentials
from ..helpers.error import ErrorResponse as Err
from ..helpers.token_parser import validate_token
from ..models.token import Token

router = APIRouter(
    prefix="/credentials",
    tags=["credentials"]
)

auth_schema = OAuth2PasswordBearer(tokenUrl="login")

# NOTE: High-risk security data is not sent by GET requests, best option is POST.

@router.post("/create-credentials", status_code=200, response_class=PlainTextResponse)
async def create_credentials(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
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
async def validate_credentials(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
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
async def delete_credentials(username: Annotated[str, Path(title="Username of the user.")],
                             token: Annotated[str, Depends(auth_schema)]):
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

    validation = await validate_token(token, username)
    if isinstance(validation, Err):
        raise HTTPException(status_code=validation.code, detail=validation.message)

    result = await utils.delete_credentials(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/update-password", status_code=200, response_class=PlainTextResponse)
async def update_password(username: Annotated[str, Path(title="Username of the user.")],
                          token: Annotated[str, Depends(auth_schema)],
                          password: Annotated[str, Form()]):
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

    validation = await validate_token(token, username)
    if isinstance(validation, Err):
        raise HTTPException(status_code=validation.code, detail=validation.message)

    result = await utils.update_password(username, password)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result