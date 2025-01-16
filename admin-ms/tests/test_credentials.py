# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# OAuth2 dependencies.
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm)

# Internal app dependencies.
from app.services import credentials_utils as utils
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc
from skladischer_auth.token_utils import create_access_token

from .helpers import (
    get_collection,
    USERNAME,
    PASSWORD)

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.credentials_utils.get_collection", get_collection)
@patch("app.services.credentials_utils.create_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.create_sensor_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_sensor_user", AsyncMock(return_value=USERNAME))
async def test_create_credentials(client, cleanup):
    """
    Test creating a new user credentials.

    Asserts:
        - The credentials creation API responds with a 200 status code.
        - The credentials creation API responds with a 400 status code if the username already exists.
    """

    # Test successful request.
    response = await client.post(url=f"/credentials/create-credentials",
                                 data={"username": USERNAME, "password": PASSWORD},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    cleanup.append(response.text)

    # Test unsuccessful request due to taken username.
    response = await client.post(url=f"/credentials/create-credentials",
                                 data={"username": USERNAME, "password": PASSWORD},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400

@pytest.mark.anyio
@patch("app.services.credentials_utils.get_collection", get_collection)
@patch("app.services.credentials_utils.create_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.create_sensor_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_sensor_user", AsyncMock(return_value=USERNAME))
async def test_validate_credentials(client, cleanup):
    """
    Test validating a user by their credentials.

    Asserts:
        - The user retrieval API responds with a 200 status code.
        - The user retrieval API responds with a 400 status code due to wrong password.
        - The user retrieval API responds with a 400 status code due to wrong username.
    """

    credentials_create = OAuth2PasswordRequestForm(username=USERNAME, password=PASSWORD)
    token = await utils.create_credentials(credentials_create)
    assert not isinstance(token, Err)
    cleanup.append(USERNAME)

    # Test unsuccessful request due to wrong password.
    response = await client.post(url=f"/credentials/login",
                                 data={"username": USERNAME, "password": "Wrong"},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

    # Test unsuccessful request due to wrong username.
    response = await client.post(url=f"/credentials/login",
                                 data={"username": "Wrong", "password": PASSWORD},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

    # Test successful request.
    response = await client.post(url=f"/credentials/login",
                                 data={"username": USERNAME, "password": PASSWORD},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.credentials_utils.get_collection", get_collection)
@patch("app.services.credentials_utils.create_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.create_sensor_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_sensor_user", AsyncMock(return_value=USERNAME))
async def test_delete_credentials(client, cleanup):
    """
    Test deleting user credentials by username.

    Asserts:
        - The user deletion API responds with a 200 status code.
        - The user retrieval API responds with a 400 status code due to wrong password.
        - The user retrieval API responds with a 400 status code due to wrong username.
    """

    credentials_create = OAuth2PasswordRequestForm(username=USERNAME, password=PASSWORD)
    username = await utils.create_credentials(credentials_create)
    assert not isinstance(username, Err)
    cleanup.append(USERNAME)

    token = await utils.validate_credentials(credentials_create)
    assert not isinstance(token, Err)

    # Test unsuccessful request due to wrong token.
    wrong_token = await create_access_token({"username": "Wrong"})
    response = await client.post(url=f"/credentials/{USERNAME}/delete-user",
                                 headers={"Authorization": f"Bearer {wrong_token}"})
    assert response.status_code == 401

    # Test unsuccessful request due to wrong username.
    response = await client.post(url=f"/credentials/Wrong/delete-user",
                                 headers={"Authorization": f"Bearer {token.access_token}"})
    assert response.status_code == 401

    # Test successful request.
    response = await client.post(url=f"/credentials/{USERNAME}/delete-user",
                                 headers={"Authorization": f"Bearer {token.access_token}"})
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.credentials_utils.get_collection", get_collection)
@patch("app.services.credentials_utils.create_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_storage_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.create_sensor_user", AsyncMock(return_value=USERNAME))
@patch("app.services.credentials_utils.delete_sensor_user", AsyncMock(return_value=USERNAME))
async def test_update_password(client, cleanup):
    """
    Test updating user password.

    Asserts:
        - The user deletion API responds with a 200 status code.
        - The user retrieval API responds with a 400 status code due to wrong token.
        - The user retrieval API responds with a 400 status code due to wrong username.
    """

    credentials_create = OAuth2PasswordRequestForm(username=USERNAME, password=PASSWORD)
    username = await utils.create_credentials(credentials_create)
    assert not isinstance(username, Err)
    cleanup.append(username)

    token = await utils.validate_credentials(credentials_create)
    assert not isinstance(token, Err)

    # Test unsuccessful request due to wrong token.
    wrong_token = await create_access_token({"username": "Wrong"})
    response = await client.post(url=f"/credentials/{USERNAME}/update-password",
                                 params={"password": "New"},
                                 headers={"Authorization": f"Bearer {wrong_token}"})
    assert response.status_code == 401

    # Test unsuccessful request due to wrong username.
    response = await client.post(url=f"/credentials/Wrong/update-password",
                                 params={"password": "New"},
                                 headers={"Authorization": f"Bearer {token.access_token}"})
    assert response.status_code == 401

    # Test successful request.
    response = await client.post(url=f"/credentials/{USERNAME}/update-password",
                                 params={"password": "New"},
                                 headers={"Authorization": f"Bearer {token.access_token}"})
    assert response.status_code == 200