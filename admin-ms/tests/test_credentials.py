# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import credentials_utils as utils
from app.schemas import credentials_schemas as schemas
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc

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
    credentials_create = schemas.CreateCredentials(username=USERNAME, password=PASSWORD).model_dump()
    response = await client.post(url="/credentials/create-credentials", json=credentials_create)
    assert response.status_code == 200
    cleanup.append(response.text)

    # Test unsuccessful request due to taken username.
    response = await client.post(url="/credentials/create-credentials", json=credentials_create)
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

    credentials_create = schemas.CreateCredentials(username=USERNAME, password=PASSWORD)
    username = await utils.create_credentials(credentials_create)
    assert not isinstance(username, Err)
    cleanup.append(username)

    # Test unsuccessful request due to wrong password.
    credentials_validate = schemas.ValidateCredentials(password="WrongPassword").model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}", json=credentials_validate)
    assert response.status_code == 403

    # Test unsuccessful request due to wrong username.
    credentials_validate = schemas.ValidateCredentials(password=PASSWORD).model_dump()
    response = await client.post(url=f"/credentials/WrongUsername", json=credentials_validate)
    assert response.status_code == 403

    # Test successful request.
    credentials_validate = schemas.ValidateCredentials(password=PASSWORD).model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}", json=credentials_validate)
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

    credentials_create = schemas.CreateCredentials(username=USERNAME, password=PASSWORD)
    username = await utils.create_credentials(credentials_create)
    assert not isinstance(username, Err)
    cleanup.append(username)

    # Test unsuccessful request due to wrong password.
    credentials_validate = schemas.ValidateCredentials(password="WrongPassword").model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}", json=credentials_validate)
    assert response.status_code == 403

    # Test unsuccessful request due to wrong username.
    credentials_validate = schemas.ValidateCredentials(password=PASSWORD).model_dump()
    response = await client.post(url=f"/credentials/WrongUsername", json=credentials_validate)
    assert response.status_code == 403

    # Test successful request.
    credentials_validate = schemas.ValidateCredentials(password=PASSWORD).model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}", json=credentials_validate)
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
        - The user retrieval API responds with a 400 status code due to wrong password.
        - The user retrieval API responds with a 400 status code due to wrong username.
    """

    credentials_create = schemas.CreateCredentials(username=USERNAME, password=PASSWORD)
    username = await utils.create_credentials(credentials_create)
    assert not isinstance(username, Err)
    cleanup.append(username)

    # Test unsuccessful request due to wrong password.
    credentials_update = schemas.UpdateCredentials(password="WrongPassword", new_password="NewPassword").model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}/update-password", json=credentials_update)
    assert response.status_code == 403

    # Test unsuccessful request due to wrong username.
    credentials_update = schemas.UpdateCredentials(password=PASSWORD, new_password="NewPassword").model_dump()
    response = await client.post(url=f"/credentials/WrongUsername/update-password", json=credentials_update)
    assert response.status_code == 403

    # Test successful request.
    credentials_update = schemas.UpdateCredentials(password=PASSWORD, new_password="NewPassword").model_dump()
    response = await client.post(url=f"/credentials/{USERNAME}/update-password", json=credentials_update)
    assert response.status_code == 200