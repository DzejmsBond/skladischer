# Author: Nina Mislej
# Date created: 08.01.2024

from pydantic import BaseModel
from typing import Optional, Dict

from .sensor_schemas import GetSensor

class UserCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new user.
    """

    username: str

class GetSensorData(BaseModel):
    """
    This schema defines the required and optional fields for getting users sensor data.
    """

    username: str
    sensors: Dict[str, GetSensor]


