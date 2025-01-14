# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..schemas import sensor_schemas, user_schemas
from ..helpers.error import ErrorResponse as Err
from ..rabitmq.sensor_data_exchange import (
    send_to_channel,
    receive_from_channel)

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

@router.post("/sensor-data", response_class=PlainTextResponse)
async def receive_sensor_data(data: dict):
    """
    API endpoint to receive sensor data and send it to RabbitMQ for processing.
    All user sensors should be sending data to this endpoint.

    Args:
        data (dict): The raw sensor data sent via HTTP POST.

    Returns:
        str: Confirmation message if successful.

    Raises:
        HTTPException: If an error occurs while sending data to RabbitMQ.
    """

    result = await send_to_channel(data)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}/sensor-data", response_model=user_schemas.GetSensorData)
async def get_sensor_data(username: str):
    """
    API endpoint to retrieve processed sensor data for a user from RabbitMQ.

    Args:
        username (str): The username for which sensor data is retrieved.

    Returns:
        user_schemas.GetSensorData: The aggregated and processed sensor data.

    Raises:
        HTTPException: If an error occurs while retrieving or processing data.
    """

    result = await receive_from_channel(username)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)
    
    return result