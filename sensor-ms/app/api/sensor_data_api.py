# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..services import sensor_utils as utils
from ..schemas import sensor_schemas as schema
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

@router.post("/sensor-data", response_class=PlainTextResponse)
async def receive_sensor_data(data: dict):

    #channel.basic_publish(
    #    exchange="sensor-data-exchange",
    #    routing_key="",
    #    body=json.dumps(data),
    #)
    return "Data received."