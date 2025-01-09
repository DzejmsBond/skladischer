# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from httpx import AsyncClient

# Internal app dependencies.
from app.services import user_utils as utils
from app.schemas import user_schemas as schemas
from app.helpers import ErrorResponse as Err

@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    user_create = schemas.UserCreate(display_name="Ana Novak").model_dump()
    response = await client.post(url="/users/create-user", json=user_create)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_item(client: AsyncClient):
    user_id = await utils.create_user(schemas.UserCreate(display_name="Ana Novak"))
    assert not isinstance(user_id, Err)
    response = await client.get(url=f"/users/{user_id}")
    assert response.status_code == 200
