# Author: Nina Mislej
# Date created: 13.01.2025

from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

class HumiditySensor(BaseModel):
    """
    Represents a humidity sensor.
    """

    type: str = "HUMIDITY"
    humidity_level: Optional[float] = None
    max_humidity: Optional[float] = None
    min_humidity: Optional[float] = None

class TemperatureSensor(BaseModel):
    """
    Represents a temperature sensor.
    """

    type: str = "TEMPERATURE"
    temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    min_temperature: Optional[float] = None

class DoorSensor(BaseModel):
    """
    Represents a door sensor.
    """

    type: str = "DOOR"
    description: Optional[str] = None
    last_opened: Optional[datetime] = None

class Sensor(BaseModel):
    """
    Represents a generic sensor.
    """

    name: str
    data: Union[HumiditySensor, TemperatureSensor, DoorSensor]