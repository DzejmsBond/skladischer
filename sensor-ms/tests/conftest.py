# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

# Internal app dependencies.
from app.api import users_api
from app.api import sensor_api
from .helpers import get_collection

app = FastAPI(title="Sensor Managment Microservice - Test")
app.include_router(users_api.router)
app.include_router(sensor_api.router)

# NOTE: Whatever is done before the yields is executed before the test function
# everything after yields is excecuted after test function.

@pytest.fixture(scope="session")
async def client():
    """
    This fixture initializes a FastAPI test client that persists across the testing session.

    Yields:
        AsyncClient: An asynchronous test client for sending API requests.
    """

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# Remove this for both asyncio and trio testing.
@pytest.fixture(scope="session")
def anyio_backend():
    """
    Specify the backend for async tests.

    Returns:
        str: The async backend to use which is `asyncio`.
    """

    return 'asyncio'

# Clean up code from database after finished.
@pytest.fixture(scope="function", autouse=True)
async def cleanup():
    """
    This fixture deletes test data created during a test function's execution.

    Yields:
        list: A list of user IDs to be cleaned up after the test.
    """

    usernames = []
    yield usernames

    db_users = await get_collection()
    if db_users is None:
        print(f" Database cleanup unsuccessful.")
        return

    result = await db_users.delete_many({"username": {"$in": usernames}})
    if not result.acknowledged:
        print(f" Database cleanup unsuccessful.")
        return

    print(f" Database cleanup successful.")
    return
