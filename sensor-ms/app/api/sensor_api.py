# Author: Nina Mislej
# Date created: 5.12.2024

# REST FastAPI dependencies.
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# Internal dependencies.
from ..services import sensor_utils as utils
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

@router.post("/{username}/create-sensor", status_code=200, response_class=PlainTextResponse)
async def create_sensor(sensor_name : str):
    """
    This endpoint allows creating new sensor for the user.

    Args:
        sensor_name (str): The name of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is created successfully.
    """

    result = await utils.create_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{username}", status_code=200, response_class=PlainTextResponse)
async def delete_sensor(sensor_name: str):
    """
    This endpoint allows deleting a sensor of the user.

    Args:
        sensor_name (str): The name of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is deleted successfully.
    """

    result = await utils.delete_sensor(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.put("/{username}", status_code=200, response_class=PlainTextResponse)
async def update_sensor_name(sensor_name: str, new_name: str):
    """
    This endpoint allows updating sensor's name.

    Args:
        sensor_name (str): The name of the sensor to be changed.
        new_name (str): The new name of the sensor.

    Raises:
        HTTPException: If an error occurs during creation.

    Returns:
        PlainTextResponse: The sensor name if it is updated successfully.
    """

    result = await utils.update_sensor_name(username, sensor_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.post("/{username}/update-password", status_code=200, response_class=PlainTextResponse)
async def update_password(username: str, credentials_schema : schema.UpdateCredentials):
    """
    This endpoint allows updating the display name of a user.

    Args:
        credentials_schema (UpdateCredentials): The credentials with new and old password.
        username (str): The user's username.

    Raises:
        HTTPException: If an error occurs during password update.

    Returns:
        PlainTextResponse: The username if the password is updated successfully.
    """

    result = await utils.update_password(username, credentials_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result