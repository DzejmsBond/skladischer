# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
# Internal dependencies.
from ..helpers.database_helpers import get_collection

router = APIRouter()

@router.get("/liveness", status_code=200, response_class=PlainTextResponse)
async def health():
    """
    This endpoint allows liveness check for Kubernetes clusters.
    """

    if await get_collection() is None:
        raise HTTPException(status_code=400, detail="Database not found.")
    return "Status OK."

# NOTE: Currently no special init conditions.
@router.get("/readiness", status_code=200, response_class=PlainTextResponse)
async def readiness():
    """
    This endpoint allows readiness check for Kubernetes clusters.
    """

    return "Status OK."