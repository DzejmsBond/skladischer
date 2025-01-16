# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse

# OAuth2 authentication dependencies.
from skladischer_auth.token_bearer import JWTBearer
from skladischer_auth.token_utils import validate_token_with_username

# Internal dependencies.
from ..services import sensor_utils as utils
from ..schemas import sensor_schemas as schema
from ..helpers.error import ErrorResponse as Err

# Logging default library.
from ..logger_setup import get_logger
logger = get_logger("sensor-ms.api")

token_bearer = JWTBearer()

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

@router.post("/{username}/create-temperature-sensor", status_code=200, response_class=PlainTextResponse)
async def create_temperature_sensor(username: str, sensor_schema: schema.TemperatureSensorCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows creating new temperature sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (TemperatureSensorCreate): The details of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    logger.debug("Create temperature sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.create_temperature_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/create-humidity-sensor", status_code=200, response_class=PlainTextResponse)
async def create_humidity_sensor(username: str, sensor_schema: schema.HumiditySensorCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows creating new humidity sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (HumiditySensorCreate): The details of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    logger.debug("Create humidity sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.create_humidity_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/create-door-sensor", status_code=200, response_class=PlainTextResponse)
async def create_door_sensor(username: str, sensor_schema: schema.DoorSensorCreate, token : str = Depends(token_bearer)):
    """
    This endpoint allows creating new door sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_schema (DoorSensorCreate): The details of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    logger.debug("Create door sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.create_door_sensor(username, sensor_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.get("/{username}/{sensor_name}", status_code=200, response_model=schema.GetSensor)
async def get_sensor(username: str, sensor_name: str, token : str = Depends(token_bearer)):
    """
    This endpoint allows fetching of a sensor for the user.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during fetching.

    Returns:
        PlainTextResponse: The sensor details if it is fetched successfully.
    """

    logger.debug("Get sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.get_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}/{sensor_name}", status_code=200, response_class=PlainTextResponse)
async def delete_sensor(username: str, sensor_name: str, token : str = Depends(token_bearer)):
    """
    This endpoint allows deleting a sensor of the user.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during deletion.

    Returns:
        PlainTextResponse: The sensor name if it is deleted successfully.
    """

    logger.debug("Delete sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.delete_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}/{sensor_name}/update-name", status_code=200, response_class=PlainTextResponse)
async def update_sensor_name(username: str, sensor_name: str, new_name: str, token : str = Depends(token_bearer)):
    """
    This endpoint allows updating sensor's name.

    Args:
        username (str): The username of the user.
        sensor_name (str): The name of the sensor to be changed.
        new_name (str): The new name of the sensor.
        token (str): Access token generated at login time.

    Raises:
        HTTPException: If an error occurs during name update.

    Returns:
        PlainTextResponse: The sensor name if it is updated successfully.
    """

    logger.debug("Update sensor endpoint request.")
    if not await validate_token_with_username(username, token):
        raise HTTPException(status_code=401, detail="Token username missmatch.")

    result = await utils.update_sensor_name(username, sensor_name, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result