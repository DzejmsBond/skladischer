# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import storage_utils, user_utils, item_utils
from app.schemas import storage_schemas, user_schemas, item_schemas
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc
from bson import ObjectId as Id
from .helpers import get_collection, get_filter_vars, USERNAME, QUERY_PATH

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
@patch("app.services.item_utils.get_collection", get_collection)
async def test_create_item(client, cleanup):
    """
    Test creating an item in a user's storage.

    Asserts:
        - The item creation API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item_create = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.").model_dump()
    response = await client.post(url=f"/users/{user_id}/{storage_name}/create-item", json=item_create)
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
@patch("app.services.item_utils.get_collection", get_collection)
async def test_get_item(client, cleanup):
    """
    Test retrieving an item by its unique code.

    Asserts:
        - The item retrieval API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)
    response = await client.get(url=f"/users/{user_id}/{storage_name}/{item_code}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
@patch("app.services.item_utils.get_collection", get_collection)
async def test_delete_item(client, cleanup):
    """
    Test deleting an item from a user's storage.

    Asserts:
        - The item deletion API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)
    response = await client.delete(url=f"/users/{user_id}/{storage_name}/{item_code}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
@patch("app.services.item_utils.get_collection", get_collection)
async def test_update_item(client, cleanup):
    """
    Test updating an item's details.

    Asserts:
        - The item update API responds with a 200 status code.
        - Updating the item amount to 0 responds with a 400 status code.
        - Cannot update an item if no fields are provided 400 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)
    update = item_schemas.ItemUpdate(description="Parmigiano.").model_dump()
    response = await client.put(url=f"/users/{user_id}/{storage_name}/{item_code}", json=update)
    assert response.status_code == 200

    # Test updating item amount to 0.
    update = item_schemas.ItemUpdate(amount=0).model_dump()
    response = await client.put(url=f"/users/{user_id}/{storage_name}/{item_code}", json=update)
    assert response.status_code == 400

    # Test updating item with zero update fields.
    response = await client.put(url=f"/users/{user_id}/{storage_name}/{item_code}", json={})
    assert response.status_code == 400

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.storage_utils.get_collection", get_collection)
@patch("app.services.item_utils.get_collection", get_collection)
async def test_filter_item(client, cleanup):
    """
    Test filtering items.

    Asserts:
        - The item update API responds with a 200 status code.
    """

    # Test successful request.
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name=USERNAME))
    assert not isinstance(user_id, Err)
    cleanup.append(Id(user_id))
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)

    # Load the query from a file.
    with open(QUERY_PATH, "r") as file:
        query = file.read()

    variables = get_filter_vars(user_id, storage_name, "Cheese", 2)
    response = await client.post(url=f"/users/", json={"query": query, "variables": variables})
    assert response.status_code == 200
    variables = get_filter_vars(user_id, storage_name, "Cheese", 1)
    response = await client.post(url=f"/users/", json={"query": query, "variables": variables})
    assert response.status_code == 200
