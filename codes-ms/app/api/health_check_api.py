# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from ..services.code_utils import check_reachable

router = APIRouter()

@router.get("/liveness", status_code=200, response_class=PlainTextResponse)
def health():
    """
    This endpoint allows liveness check for Kubernetes clusters.
    """

    if not check_reachable():
        raise HTTPException(status_code=400, detail="QR code api not reachable.")
    return "Status OK."

# NOTE: Currently no special init conditions.
@router.get("/readiness", status_code=200, response_class=PlainTextResponse)
def readiness():
    """
    This endpoint allows rediness check for Kubernetes clusters.
    """

    return "Status OK."