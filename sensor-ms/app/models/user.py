# Author: Nina Mislej
# Date created: 13.01.2025

from pydantic import BaseModel
from typing import Optional, List, Union
from .sensors import HumiditySensor, TemperatureSensor, DoorSensor


class User(BaseModel):
    """
    Represents a user with a list of currently supported sensors.
    """

    username: str
    sensors: List[Union[HumiditySensor, TemperatureSensor, DoorSensor]]