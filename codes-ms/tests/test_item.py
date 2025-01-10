# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from httpx import AsyncClient

# Internal app dependencies.
from app.services import storage_utils
from app.services import user_utils
from app.services import item_utils
from app.schemas import storage_schemas
from app.schemas import user_schemas
from app.schemas import item_schemas
from app.helpers import ErrorResponse as Err

@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item_create = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.").model_dump()
    response = await client.post(url=f"/users/{user_id}/{storage_name}/create-item", json=item_create)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_item(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)
    response = await client.get(url=f"/users/{user_id}/{storage_name}/{item_code}")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete_item(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    storage_name = await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(storage_name, Err)
    item = item_schemas.ItemCreate(name="Cheese", amount=2, description="Cheddar.")
    item_code = await item_utils.create_item(user_id, storage_name, item)
    assert not isinstance(item_code, Err)
    response = await client.delete(url=f"/users/{user_id}/{storage_name}/{item_code}")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_update_item(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
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
