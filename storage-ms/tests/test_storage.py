# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from httpx import AsyncClient

# Internal app dependencies.
from app.services import storage_utils
from app.services import user_utils
from app.schemas import storage_schemas
from app.schemas import user_schemas
from app.helpers import ErrorResponse as Err

@pytest.mark.anyio
async def test_create_storage(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    storage_create = storage_schemas.StorageCreate(name="Fridge").model_dump()
    response = await client.post(url=f"/users/{user_id}/create-storage", json=storage_create)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_storage(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(user_id, Err)
    response = await client.get(url=f"/users/{user_id}/Fridge")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete_storage(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(user_id, Err)
    response = await client.delete(url=f"/users/{user_id}/Fridge")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_update_storage_name(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(user_id, Err)
    response = await client.put(url=f"/users/{user_id}/Fridge/update-name", params={"new_name": "Freezer"})
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete_storage_items(client: AsyncClient):
    user_id = await user_utils.create_user(user_schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    await storage_utils.create_storage(user_id, storage_schemas.StorageCreate(name="Fridge"))
    assert not isinstance(user_id, Err)
    response = await client.put(url=f"/users/{user_id}/Fridge/empty-storage")
    assert response.status_code == 200