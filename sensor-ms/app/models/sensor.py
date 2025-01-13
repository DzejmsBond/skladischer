# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    """
    Represents a user with a list of sensor names.
    """

    username: str
    sensors: List[str]