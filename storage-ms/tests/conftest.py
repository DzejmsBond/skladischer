# Author: Nina Mislej
# Date created: 09.01.2025

import pytest
from mongomock import MongoClient
from app.models.user import User
from unittest.mock import patch


@pytest.fixture
@patch("app.helpers.database_helpers.get_collection")
def get_collection():
    client = MongoClient()
    database = client["test-database"]

    with patch("app.helpers.database_helpers.get_collection",
               new=AsyncMock(return_value=database["users"])) as collection:
        yield collection