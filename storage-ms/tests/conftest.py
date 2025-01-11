# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

# Enable GraphQL
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from pathlib import Path

# Internal app dependencies.
from app.api import users_api
from app.api import storage_api
from app.api import item_api
from app.graphql import resolvers
from .helpers import get_collection, USERNAME, NEW_USERNAME

app = FastAPI(title="Storage Managment Microservice - Test")
app.include_router(users_api.router)
app.include_router(storage_api.router)
app.include_router(item_api.router)

# Used by graphQL to create schemas.
path = Path(__file__).resolve().parent.parent / 'app' / 'graphql' / 'schemas.graphql'
type_defs = load_schema_from_path(path)
schema = make_executable_schema(type_defs, [resolvers.query, resolvers.items])
app.mount("/users/", GraphQL(schema))

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

    user_ids = []
    yield user_ids

    db_users = await get_collection()
    if db_users is None:
        print(f" Database cleanup unsuccessful.")
        return

    result = await db_users.delete_many({"_id": {"$in": user_ids}})
    if not result.acknowledged:
        print(f" Database cleanup unsuccessful.")
        return

    print(f" Database cleanup successful.")
    return
