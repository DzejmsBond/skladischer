# Author: Nina Mislej
# Date created: 08.01.2024

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new user.
    """

    username: str