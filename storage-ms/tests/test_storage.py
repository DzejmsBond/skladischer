# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import storage_utils, user_utils
from app.schemas import storage_schemas, user_schemas
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc
from bson import ObjectId as Id
from .helpers import get_collection, USERNAME

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
async def test_create_storage(client, cleanup):
    """
    Test creating a storage for a user.

    Asserts:
        - The storage creation API responds with a 200 status code.
        - The storage cannot be created if name already exists, returns 409 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_create = storage_schemas.StorageCreate(name="Fridge").model_dump()
    response = await client.post(url=f"/users/{user_id}/create-storage", json=storage_create)
    assert response.status_code == 200

    # Test duplicated name unsuccessful request.
    response = await client.post(url=f"/users/{user_id}/create-storage", json=storage_create)
    assert response.status_code == 409

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
async def test_get_storage(client, cleanup):
    """
    Test retrieving a storage by its name.

    Asserts:
        - The storage retrieval API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    response = await client.get(url=f"/users/{user_id}/Fridge")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
async def test_delete_storage(client, cleanup):
    """
    Test deleting a storage by its name.

    Asserts:
        - The storage deletion API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    response = await client.delete(url=f"/users/{user_id}/Fridge")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
async def test_update_storage_name(client, cleanup):
    """
    Test updating a storage's name.

    Asserts:
        - The storage name update API responds with a 200 status code.
        - The storage cannot be updated if name already exists, returns 409 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    response = await client.put(url=f"/users/{user_id}/Fridge/update-name", params={"new_name": "Freezer"})
    assert response.status_code == 200

    # Test duplicated name unsuccessful request.
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Shelf"))
    response = await client.put(url=f"/users/{user_id}/Freezer/update-name", params={"new_name": "Shelf"})
    assert response.status_code == 409

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
async def test_delete_storage_items(client, cleanup):
    """
    Test clearing all items in a storage.

    Asserts:
        - The storage clearing API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    response = await client.put(url=f"/users/{user_id}/Fridge/empty-storage")
    assert response.status_code == 200