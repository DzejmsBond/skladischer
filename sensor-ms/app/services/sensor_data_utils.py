# Author: Nina Mislej
# Date created: 13.01.2025

from ..schemas import sensor_schemas, user_schemas
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from ..services import sensor_utils as utils
from typing import Tuple

from ..models.sensors import (
    HumiditySensor,
    DoorSensor,
    TemperatureSensor,
    Sensor)

from ..models.sensors import TEMPERATURE, HUMIDITY, DOOR
from datetime import datetime, timezone

async def process_queue(username: str, queue: list) -> Err | user_schemas.GetSensorData:
    try:
        response = user_schemas.GetSensorData(username=username, sensors={})
        for entry in queue:
            await post_process_data(entry, response)

        for sensor in response.sensors.values():
            if sensor.data.type == TEMPERATURE:
                sensor.data.temperature = round(sensor.data.temperature / sensor.count, 2)
            if sensor.data.type == HUMIDITY:
                sensor.data.humidity_level = round(sensor.data.humidity_level / sensor.count, 2)
        return response

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def pre_process_data(data: dict) -> Err | dict | None:
    try:
        result = await get_valid_sensor(data)
        if isinstance(result, Err):
            return result

        sensor_type, sensor = result
        if sensor_type == TEMPERATURE:
            return data
        elif sensor_type == HUMIDITY:
            return data
        elif sensor_type == DOOR:
            return await process_door(data.get("username"), sensor)

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def post_process_data(data: dict, response: user_schemas.GetSensorData) -> None | Err:
    try:
        sensor_type, sensor = await get_valid_sensor(data)
        if sensor_type == TEMPERATURE:
            return await process_temperature(data, sensor, response)
        elif sensor_type == HUMIDITY:
            return await process_humidity(data, sensor, response)

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def get_valid_sensor(data: dict) -> Tuple[str, Sensor] | Err:

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        if "name" not in data:
            return Err(message=f"Missing name of the sensor in data.", code=400)

        if "username" not in data:
            return Err(message=f"Missing username in data.", code=400)

        sensor_dict = await utils.get_sensor(data.get("username"), data.get("name"))
        if isinstance(sensor_dict, Err):
            return sensor_dict

        if "data" not in sensor_dict:
            return Err(message=f"Missing data in sensor: {data.get("name")}.", code=400)

        stored_data = sensor_dict["data"]
        if "type" not in stored_data:
            return Err(message=f"Missing type in sensor: {data.get('name')}.", code=400)

        sensor = Sensor(**sensor_dict)
        return stored_data["type"], sensor

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def process_door(username: str, sensor: Sensor) -> Err | str :

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")


        result = await db_users.update_one(
            {"username": username,
             "sensors.name": sensor.name},
            {"$set": {f"sensors.$.data.last_opened": datetime.now(tz=timezone.utc)}})

        if not result.acknowledged or result.modified_count == 0:
            return Err(message=f"Door Sensor {sensor.name} not updated.", code=404)
        return sensor.name

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def process_temperature(data: dict, sensor: Sensor, response: user_schemas.GetSensorData) -> None | Err:

    try:
        if "temperature" not in data:
            return Err(message=f"Missing temperature in data: {sensor.name}.", code=400)
        else:
            temperature = data.get("temperature")

            if sensor.name not in response.sensors:
                response.sensors[sensor.name] = sensor_schemas.GetSensor(name=sensor.name,
                                                                         data=sensor.data,
                                                                         details=[])
                response.sensors[sensor.name].data.temperature = 0

            response_sensor = response.sensors[sensor.name]
            response_sensor.count += 1
            response_sensor.data.temperature += temperature
            if sensor.data.max_temperature and temperature > sensor.data.max_temperature:
                response_sensor.details.append(f"Temperature over limit: {temperature}")
            if sensor.data.min_temperature and temperature < sensor.data.min_temperature:
                response_sensor.details.append(f"Temperature under limit: {temperature}")
            return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def process_humidity(data: dict, sensor: Sensor, response: user_schemas.GetSensorData) -> None | Err:

    try:
        if "humidity_level" not in data:
            return Err(message=f"Missing humidity level in data: {sensor.name}.", code=400)
        else:
            humidity = data.get("humidity_level")

            if sensor.name not in response.sensors:
                response.sensors[sensor.name] = sensor_schemas.GetSensor(name=sensor.name, data=sensor.data)
                sensor.data.humidity_level = 0

            response_sensor = response.sensors[sensor.name]
            response_sensor.count += 1
            response_sensor.data.humidity_level += humidity
            if sensor.data.max_humidity and humidity > sensor.data.max_humidity:
                response[sensor.name].details.append(f"Humidity over limit: {humidity}")
            if sensor.data.min_humidity and humidity < sensor.data.min_humidity:
                response[sensor.name].details.append(f"Humidity under limit: {humidity}")
            return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)