# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse

# OAuth2 authentication dependencies.
from auth.token_bearer import JWTBearer
from auth.token_utils import validate_token_with_username

# Internal dependencies.
from ..services import code_utils as utils
from ..helpers.error import ErrorResponse as Err
from ..schemas import code_schemas as schema

token_bearer = JWTBearer()

router = APIRouter(
    prefix="/codes",
    tags=["codes"]
)

@router.post("/create-code", status_code=200, response_class=PlainTextResponse)
async def create_code(code_schema : schema.CodeCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows the creation of a new item code.

    Args:
        code_schema (ItemCreate): The code details to be created.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during item creation.

    Returns:
        PlainTextResponse: The encoded QR code image in string format.
    """

    result = await utils.create_code(code_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result