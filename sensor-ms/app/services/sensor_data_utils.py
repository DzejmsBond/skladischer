# Author: Nina Mislej
# Date created: 13.01.2025

from ..schemas import sensor_schemas as schema
from ..models.sensors import HumiditySensor, DoorSensor, TemperatureSensor, Sensor
from ..helpers.database_helpers import get_collection
from ..helpers.error import ErrorResponse as Err
from ..services.sensor_utils import get_sensor

from datetime import datetime, timezone

async def process_queue(username: str, queue: list) -> Err | Sensor:

    try:
        return Err(message="Not implemented.")

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)

async def process_data(data: dict) -> Err | dict | None:

    try:
        db_users = await get_collection()
        if db_users is None:
            return Err(message=f"Cannot get DB collection.")

        if "name" not in data:
            return Err(message=f"Missing name of the sensor in data.", code=400)

        if "username" not in data:
            return Err(message=f"Missing username in data.", code=400)

        sensor = await get_sensor(data.get("username"), data.get("name"))
        if isinstance(sensor, Err):
            return sensor

        if "data" not in sensor:
            return Err(message=f"Missing data in sensor: {data.get("name")}.", code=400)

        stored_data = sensor["data"]
        if "type" not in stored_data:
            return Err(message=f"Missing type in sensor: {data.get('name')}.", code=400)

        sensor_type = stored_data["type"]
        if sensor_type == "TEMPERATURE":
            return data
        elif sensor_type == "HUMIDITY":
            return data
        elif sensor_type == "DOOR":
            result = await db_users.update_one(
                {"username": username, "sensors.name": data.get('name')},
                {"$set": {f"sensors.$.last_opened": datetime.now(tz=timezone.utc)}})
            if not result.acknowledged or result.modified_count == 0:
                return Err(message=f"Door Sensor {data.get('name')} not updated.", code=404)
            return None

    except Exception as e:
        return Err(message=f"Unknown exception: {e}", code=500)
