# Author: Nina Mislej
# Date created: 13.01.2025

from typing import Any, Mapping

from ..schemas import sensor_schemas as schema
from ..models.sensors import HumiditySensor, DoorSensor, TemperatureSensor, Sensor
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err

async def create_humidity_sensor(username: str, sensor : schema.HumiditySensorCreate) -> Err | str:
    """
    Create a new humidity sensor in the database.

    This function inserts a new user sensor into the database. If the operation fails for
    any reason, an error response is returned.

    Args:
        username (str): The userername of the user creating the sensor.
        sensor (HumiditySensorCreate): The data of the sensor to be created.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or name of the sensor otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        data = HumiditySensor(max_humidity=sensor.max_humidity,
                                      min_humidity=sensor.min_humidity)

        sensor_dict = Sensor(name=sensor.name, data=data)

        if not isinstance(await get_sensor(username, sensor.name), Err):
            return Err(message=f"Sensor name '{sensor.name}' already exists and cannot be created.", code=409)

        result = await db_users.update_one({"username": username},
                                           {"$push": {"sensors": sensor_dict}})
        if not result.acknowledged:
            return Err(message=f"Creating sensor '{sensor.name}' failed.")

        if result.modified_count == 0:
            return Err(message=f"Creating sensor '{sensor.name}' modified zero entries.")
        return sensor.name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def create_temperature_sensor(username: str, sensor : schema.TemperatureSensorCreate) -> Err | str:
    """
    Create a new temperature sensor in the database.

    This function inserts a new user sensor into the database. If the operation fails for
    any reason, an error response is returned.

    Args:
        username (str): The userername of the user creating the sensor.
        sensor (HumiditySensorCreate): The data of the sensor to be created.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or name of the sensor otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        data = TemperatureSensor(max_temperature=sensor.max_temperature,
                                min_temperature=sensor.min_temperature)

        sensor_dict = Sensor(name=sensor.name, data=data)

        if not isinstance(await get_sensor(username, sensor.name), Err):
            return Err(message=f"Sensor name '{sensor.name}' already exists and cannot be created.", code=409)

        result = await db_users.update_one({"username": username},
                                           {"$push": {"sensors": sensor_dict}})
        if not result.acknowledged:
            return Err(message=f"Creating sensor '{sensor.name}' failed.")

        if result.modified_count == 0:
            return Err(message=f"Creating sensor '{sensor.name}' modified zero entries.")
        return sensor.name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def create_door_sensor(username: str, sensor : schema.DoorSensorCreate) -> Err | str:
    """
    Create a new door sensor in the database.

    This function inserts a new user credentials into the database. If the operation fails for
    any reason, an error response is returned.

    Args:
        username (str): The userername of the user creating the sensor.
        sensor (HumiditySensorCreate): The data of the sensor to be created.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or name of the sensor otherwise.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        data = DoorSensor(description=sensor.description)
        sensor_dict = Sensor(name=sensor.name, data=data)

        if not isinstance(await get_sensor(username, sensor.name), Err):
            return Err(message=f"Sensor name '{sensor.name}' already exists and cannot be created.", code=409)

        result = await db_users.update_one({"username": username},
                                           {"$push": {"sensors": sensor_dict}})
        if not result.acknowledged:
            return Err(message=f"Creating sensor '{sensor.name}' failed.")

        if result.modified_count == 0:
            return Err(message=f"Creating sensor '{sensor.name}' modified zero entries.")
        return sensor.name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def get_sensor(username: str, name : str) -> Err | dict:
    """
       Retrieve a sensor by its name for a specific user.

       This function fetches a sensor object for a user based on the `name`.
       If the sensor does not exist or the operation fails, an error response is returned.

       Args:
           username (str): The username of the user who owns the sensor.
           name (str): The name of the sensor to retrieve.

       Returns:
           ErrorResponse | dict: The error response if an error occurred, or the sensor details as a dictionary.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        # A cleaner way of finding all matchings and a sanity check that there are unique.
        pipeline = [
            {"$match": {"username": username}}, # Finds the user.
            {"$unwind": "$sensors"},  # Deconstruct the sensors array.
            {"$match": {"sensors.name": name}}, # Match the specific sensor.
            {"$replaceRoot": {"newRoot": "$sensors"}}  # Replace the root document with the sensor object.
        ]

        result = await db_users.aggregate(pipeline).to_list()
        if not result:
            return Err(message=f"Getting sensor '{name}' failed.")

        if len(result) > 1:
            return Err(message=f"Sensor '{name}' has more than one storage entry.")

        result_dict = result[0]
        if "name" not in result_dict or "data" not in result_dict:
            return Err(message=f"Aquired sensor has no name or data.")

        return schema.GetSensor(name=result_dict["name"], data=result_dict["data"]).model_dump()

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def delete_sensor(username : str, name : str) -> Err | str:
    """
    Delete a sensor by its name for a specific user.

    This function removes a sensor object from a user's list of sensors based
    on the `name`. If the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the sensor.
        name (str): The name of the sensor to delete.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or sensor name if the deletion was successful.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        result = await db_users.update_one(
            {"username": username},
            {"$pull": {"sensors": {"name": name}}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Deleting sensor '{name}' failed.")
        return name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)


async def update_sensor_name(username : str, name : str, new_name : str) -> Err | str:
    """
    Update the name of a sensor for a specific user.

    This function changes the name of a sensor in a user's sensors list.
    If the new name already exists or the operation fails, an error response is returned.

    Args:
        username (str): The username of the user who owns the sensor.
        name (str): The current name of the sensor to update.
        new_name (str): The new name for the sensor.

    Returns:
        ErrorResponse | str: The error response if an error occurred, or sensor name if the update was successful.
    """
    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        if not isinstance(await get_sensor(username, new_name), Err):
            return Err(message=f"Sensor name '{new_name}' already exists.", code=409)

        result = await db_users.update_one(
            {"username": username, "sensors.name": name},
            {"$set": {"sensors.$.name": new_name}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Updating sensor name '{name}' with '{new_name}' failed.")
        return new_name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

