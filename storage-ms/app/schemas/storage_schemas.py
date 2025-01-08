# Author: Nina Mislej
# Date created: 07.01.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional

class StorageCreate(BaseModel):
    """
    This schema defines the required field for creating a new storage.
    """

    name: str

