# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from ..services import code_utils as utils
from ..helpers.error import ErrorResponse as Err
from ..schemas import code_schemas as schema

router = APIRouter(
    prefix="/codes",
    tags=["codes"]
)

@router.post("/create-code", status_code=200, response_class=PlainTextResponse)
async def create_code(code_schema : schema.CodeCreate):
    """
    This endpoint allows the creation of a new item code.

    Args:
        code_schema (ItemCreate): The code details to be created.

    Raises:
        HTTPException: If an error occurs during item creation.

    Returns:
        PlainTextResponse: The encoded QR code image in string format.
    """

    result = await utils.create_code(code_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result