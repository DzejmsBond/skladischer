# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

# Internal app dependencies.
from app.api import users_api
from app.api import storage_api
from app.api import item_api
from .helpers import get_collection, USERNAME, NEW_USERNAME

app = FastAPI(title="Storage Managment Microservice - Test")
app.include_router(users_api.router)
app.include_router(storage_api.router)
app.include_router(item_api.router)

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# Remove this for both asyncio and trio testing.
@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

# Clean up code from database after finished.
@pytest.fixture(scope="function", autouse=True)
async def cleanup():
    yield
    # Delete all users with display_name USERNAME or NEW_USERNAME.
    db_users = await get_collection()
    if db_users is None:
        print(f" Database cleanup unsuccessful.")
        return

    result = await db_users.delete_many({"display_name": USERNAME})
    if not result.acknowledged:
        print(f" Database cleanup unsuccessful.")
        return

    result = await db_users.delete_many({"display_name": NEW_USERNAME})
    if not result.acknowledged:
        print(f" Database cleanup unsuccessful.")
        return

    print(f" Database cleanup successful.")
    return
