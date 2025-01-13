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

@router.post("/{username}/create-temperature-sensor", status_code=200, response_class=PlainTextResponse)
async def create_temperature_sensor(username: str, sensor_schema: schema.TemperatureSensorCreate):
    """
    This endpoint allows creating new temperature sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (TemperatureSensorCreate): The details of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    result = await utils.create_temperature_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/create-humidity-sensor", status_code=200, response_class=PlainTextResponse)
async def create_humidity_sensor(username: str, sensor_schema: schema.HumiditySensorCreate):
    """
    This endpoint allows creating new humidity sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (HumiditySensorCreate): The details of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    result = await utils.create_humidity_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/create-door-sensor", status_code=200, response_class=PlainTextResponse)
async def create_door_sensor(username: str, sensor_schema: schema.DoorSensorCreate):
    """
    This endpoint allows creating new door sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (DoorSensorCreate): The details of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    result = await utils.create_door_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}/{sensor_name}", status_code=200, response_model=schema.GetSensor)
async def get_sensor(username: str, sensor_name: str):
    """
    This endpoint allows fetching of a sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor.

    Raises:
        HTTPException: If an error occurs during fetching.

    Returns:
        PlainTextResponse: The sensor details if it is fetched successfully.
    """

    result = await utils.get_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}/{sensor_name}", status_code=200, response_class=PlainTextResponse)
async def delete_sensor(username: str, sensor_name: str):
    """
    This endpoint allows deleting a sensor of the user.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor.

    Raises:
        HTTPException: If an error occurs during deletion.

    Returns:
        PlainTextResponse: The sensor name if it is deleted successfully.
    """

    result = await utils.delete_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/{sensor_name}", status_code=200, response_class=PlainTextResponse)
async def update_sensor_name(username: str, sensor_name: str, new_name: str):
    """
    This endpoint allows updating sensor's name.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor to be changed.
        new_name (str): The new name of the sensor.

    Raises:
        HTTPException: If an error occurs during name update.

    Returns:
        PlainTextResponse: The sensor name if it is updated successfully.
    """

    result = await utils.update_sensor_name(username, sensor_name, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result