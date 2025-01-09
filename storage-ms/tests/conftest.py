# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from mongomock import MongoClient

# Internal app dependencies.
from app.api import users_api
from app.api import storage_api
from app.api import item_api

app = FastAPI(title="Storage Managment Microservice - Test")
app.include_router(users_api.router)
app.include_router(storage_api.router)
app.include_router(item_api.router)

@pytest.fixture(scope="session")
async def get_collection():
    client = MongoClient()
    database = client["test-database"]
    collection = database["users"]

    async with patch("app.helpers.database_helpers.get_collection",
               new=AsyncMock(return_value=collection)) as mock:
        yield mock


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# Remove this for asyncio and trio testing.
@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'