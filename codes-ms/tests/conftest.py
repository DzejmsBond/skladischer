# Author: Nina Mislej
# Date created: 09.01.2025

# Mimic generated image.
import os
import base64

# Enable async testing.
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

# Internal app dependencies.
from app.api import code_api

app = FastAPI(title="Code Generation Microservice - Test")
app.include_router(code_api.router)

# NOTE: Whatever is done before the yields is executed before the test function
# everything after yields is excecuted after test function.

@pytest.fixture(scope="session")
async def encoded_image():
    """
    Mimics the encoded image in order to avoid third party API calls in tests.

    Yields:
        AsyncClient: An asynchronous test client for sending API requests.
    """

    random_bytes = os.urandom(30)
    encoded = base64.b64encode(random_bytes)
    yield encoded

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