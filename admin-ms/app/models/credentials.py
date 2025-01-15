# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

# Hashing the password
from bcrypt import hashpw, gensalt

class Credentials(BaseModel):
    """
    Represents a user model in admin environment.
    Password is already hashed at this stage.
    """

    username: str
    password: str

    @field_validator('password', mode="before")
    @classmethod
    def hash_password(cls, ps):
        return hashpw(ps.encode('utf8'), gensalt()).decode('utf8')

