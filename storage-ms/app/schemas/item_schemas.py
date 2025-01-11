# Author: Nina Mislej
# Date created: 07.01.2024

from pydantic import BaseModel
from typing import Optional

# These are pydantic models used by FastAPI.

class ItemCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new item.
    """

    name: str
    amount: Optional[int] = None
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    """
    This schema defines the fields that can be updated for an existing item.
    """

    name: Optional[str] = None
    amount: Optional[int] = None
    description: Optional[str] = None
