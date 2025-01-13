# Author: Nina Mislej
# Date created: 08.01.2024

from pydantic import BaseModel
from typing import Optional

class HumiditySensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new humidity sensor.
    """

    name: str
    max_humidity: Optional[float]
    min_humidity: Optional[float]

class TemperatureSensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new temperature sensor.
    """

    name: str
    max_temperature: Optional[float]
    min_temperature: Optional[float]

class DoorSensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new door sensor.
    """

    name: str
    open: Optional[bool]
    description: Optional[str] = None