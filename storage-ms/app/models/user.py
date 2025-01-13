# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .storage import Storage

class User(BaseModel):
    """
    Represents a user model.
    This model defines the attributes of a user, including their username, display name and the list of storages they own.
    While display name is optional, username is required.
    """

    username: str
    display_name: Optional[str] = None
    storages: List[Storage]