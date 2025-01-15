# Author: Nina Mislej
# Date created: 08.01.2024

from pydantic import BaseModel
from typing import Optional, Union, List
from ..models import HumiditySensor, TemperatureSensor, DoorSensor

class HumiditySensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new humidity sensor.
    """

    name: str
    max_humidity: Optional[float] = None
    min_humidity: Optional[float] = None

class TemperatureSensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new temperature sensor.
    """

    name: str
    max_temperature: Optional[float] = None
    min_temperature: Optional[float] = None

class DoorSensorCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new door sensor.
    """

    name: str
    description: Optional[str] = None

class GetSensor(BaseModel):
    """
    Retrieving the sensor data from the sensor services.
    """

    name: str
    data: Union[HumiditySensor, TemperatureSensor, DoorSensor]
    details: Optional[List[str]] = None
    count: int = 0