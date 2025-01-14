# Author: Nina Mislej
# Date created: 13.01.2025

from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal
from datetime import datetime

TEMPERATURE = "TEMPERATURE"
HUMIDITY = "HUMIDITY"
DOOR = "DOOR"

class HumiditySensor(BaseModel):
    """
    Represents a humidity sensor.
    """

    type: Literal[HUMIDITY] = HUMIDITY
    humidity_level: Optional[float] = None
    max_humidity: Optional[float] = None
    min_humidity: Optional[float] = None

class TemperatureSensor(BaseModel):
    """
    Represents a temperature sensor.
    """

    type: Literal[TEMPERATURE] = TEMPERATURE
    temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    min_temperature: Optional[float] = None

class DoorSensor(BaseModel):
    """
    Represents a door sensor.
    """

    type: Literal[DOOR] = DOOR
    description: Optional[str] = None
    last_opened: Optional[datetime] = None

class Sensor(BaseModel):
    """
    Represents a generic sensor.
    """

    name: str
    data: Union[HumiditySensor, TemperatureSensor, DoorSensor] = Field(discriminator="type")