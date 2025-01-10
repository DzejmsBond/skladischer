# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import code_utils
from app.schemas import code_schemas
from app.helpers import ErrorResponse as Err
from bson import ObjectId as Id

# NOTE: Here is a different example of patching where a fixture is used in order to support async mock.
# Could be done like in Storage microservice but this shows another useful way of doing it.

@pytest.mark.anyio
async def test_create_code(client, encoded_image):
    """
    Test creating a QR code based on user.

    Asserts:
        - The item creation API responds with a 200 status code.
    """

    # Test successful request.
    with patch("app.services.code_utils.get_code", AsyncMock(return_value=encoded_image)):
        code_id =  str(Id())
        code_data = code_schemas.CodeCreate(code_id=code_id, label="test code").model_dump()
        response = await client.post(url=f"/codes/create-code", json=code_data)
        assert response.status_code == 200
