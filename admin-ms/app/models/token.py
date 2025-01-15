# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List

class Token(BaseModel):
    """
    Represents a token used to verify user credentials.
    """

    access_token: str
    token_type: str

