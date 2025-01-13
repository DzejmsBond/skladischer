# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import user_utils as utils
from app.schemas import user_schemas as schemas
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc
from .helpers import get_collection, USERNAME, DISPLAYNAME

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_create_user(client, cleanup):
    """
    Test creating a new user.

    Asserts:
        - The user creation API responds with a 200 status code.
        - The user creation API responds with 402 status code due to duplicated username.
    """

    # Test successful request.
    user_create = schemas.UserCreate(username=USERNAME).model_dump()
    response = await client.post(url="/users/create-user", json=user_create)
    assert response.status_code == 200
    cleanup.append(response.text)

    # Test unsuccessful request.
    response = await client.post(url="/users/create-user", json=user_create)
    assert response.status_code == 402

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_get_user(client, cleanup):
    """
    Test retrieving a user by their ID.

    Asserts:
        - The user retrieval API responds with a 200 status code.
    """

    # Test successful request.
    username = await utils.create_user(schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    response = await client.get(url=f"/users/{username}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_delete_user(client, cleanup):
    """
    Test deleting a user by their ID.

    Asserts:
        - The user deletion API responds with a 200 status code.
    """

    # Test successful request.
    username = await utils.create_user(schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    response = await client.delete(url=f"/users/{username}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_update_user_name(client, cleanup):
    """
    Test updating a user's display name.

    Asserts:
        - The display name update API responds with a 200 status code.
    """

    # Test successful request.
    username = await utils.create_user(schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    response = await client.put(url=f"/users/{username}/update-name", params={"new_name": DISPLAYNAME})
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_delete_user_storages(client, cleanup):
    """
    Test clearing all storages for a user.

    Asserts:
        - The user storage clearing API responds with a 200 status code.
    """

    # Test successful request.
    username = await utils.create_user(schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    response = await client.put(url=f"/users/{username}/empty-storages")
    assert response.status_code == 200