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
from bson import ObjectId as Id
from .helpers import get_collection, USERNAME, NEW_USERNAME

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_create_user(client, cleanup):
    """
    Test creating a new user.

    Asserts:
        - The user creation API responds with a 200 status code.
    """

    # Test successful request.
    user_create = schemas.UserCreate(display_name=USERNAME).model_dump()
    response = await client.post(url="/users/create-user", json=user_create)
    assert response.status_code == 200
    cleanup.append(Id(response.text))

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
async def test_get_user(client, cleanup):
    """
    Test retrieving a user by their ID.

    Asserts:
        - The user retrieval API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await utils.create_user(schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    response = await client.get(url=f"/users/{user_id}")
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
    user_id = await utils.create_user(schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    response = await client.delete(url=f"/users/{user_id}")
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
    user_id = await utils.create_user(schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    response = await client.put(url=f"/users/{user_id}/update-name", params={"new_name": NEW_USERNAME})
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
    user_id = await utils.create_user(schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    response = await client.put(url=f"/users/{user_id}/empty-storages")
    assert response.status_code == 200