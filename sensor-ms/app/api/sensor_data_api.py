# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..services import sensor_data_utils as utils
from ..schemas import sensor_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..rabitmq.sensor_data_exchange import send_to_channel

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

@router.post("/sensor-data", response_class=PlainTextResponse)
async def receive_sensor_data(data: dict):

    processed_data = await utils.process_data(data)
    if isinstance(processed_data, Err):
        raise HTTPException(status_code=processed_data.code, detail=processed_data.message)
    if not processed_data:
        return "Data recieved and processed."

    await send_to_channel(processed_data.get("username"), processed_data)
    return "Data received and forwarded."