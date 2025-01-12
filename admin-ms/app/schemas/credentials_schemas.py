# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

# Hashing the password
from bcrypt import hashpw, gensalt

class CreateCredentials(BaseModel):
    """
    This schema defines the fields required to create a new user.
    Password is encrypted as soon as possible.
    """

    username: str
    password: str

    @field_validator('password', mode="before")
    @classmethod
    def hash_password(cls, ps):
        return hashpw(ps.encode('utf8'), gensalt()).decode('utf8')

class ValidateCredentials(BaseModel):
    """
    This schema defines the fields required to validate a user.
    Password is encrypted as soon as possible.
    """

    password: str

class UpdateCredentials(BaseModel):
    """
    This schema defines the fields required to create a new user.
    Password is encrypted as soon as possible.
    """

    password: str
    new_password: str

    @field_validator('new_password', mode='before')
    @classmethod
    def hash_password(cls, ps: str) -> str:
        return hashpw(ps.encode('utf8'), gensalt()).decode('utf8')


