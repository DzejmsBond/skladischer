# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    """
    This schema defines the optional fields for creating a new user.
    If the user does not specify a ``display_name`` the username will be used.
    """

    username: str
    display_name: Optional[str] = None


