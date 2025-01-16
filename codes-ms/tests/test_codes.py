# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import code_utils
from app.schemas import code_schemas
from app.helpers import ErrorResponse as Err
from bson import ObjectId as Id

from auth.token_utils import create_access_token

# NOTE: Here is a different example of patching where a fixture is used in order to support async mock.
# Could be done like in Storage microservice but this shows another useful way of doing it.

@pytest.mark.anyio
async def test_create_code(client, encoded_image):
    """
    Test creating a QR code based on user.
    The call to the code generation API is mimicked in order to avoid third party API calls in tests.

    Asserts:
        - The item creation API responds with a 200 status code.
    """

    # Test successful request.
    with patch("app.services.code_utils.generate_code", AsyncMock(return_value=encoded_image)):
        code_id =  str(Id())
        token = await create_access_token({"username": "GenericUser"})
        code_data = code_schemas.CodeCreate(code_id=code_id, label="test code").model_dump()
        response = await client.post(url=f"/codes/create-code",
                                     headers={"Authorization": f"Bearer {token}"},
                                     json=code_data)
        assert response.status_code == 200
