# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List

class Credentials(BaseModel):
    """
    Represents a user model in admin environment.
    Password is already hashed at this stage.
    """

    username: str
    password: str

