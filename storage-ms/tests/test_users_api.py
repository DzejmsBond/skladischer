# Author: Nina Mislej
# Date created: 09.01.2025

from unittest import TestCase
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import users_api
from app.schemas import user_schemas as schemas

app = FastAPI(
    title="Storage Managment Microservice - Test"
)

app.include_router(users_api.router)
client = TestClient(app)

def test_create_item():
    user_create = schemas.UserCreate(display_name="Ana Novak").model_dump()
    response = client.post(url="/users/create-user", json=user_create)
    assert response.status_code == 200

