"""
The `schemas` module serves as a model transfering JSON information from requests to proper models used in database.
"""

from .user_schemas import (
    UserCreate,
    GetSensorData)

from .sensor_schemas import (
    HumiditySensorCreate,
    TemperatureSensorCreate,
    DoorSensorCreate,
    GetSensor)