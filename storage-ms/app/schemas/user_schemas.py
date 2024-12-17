# Author: Jure
# Date created: 4.12.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    ref_id: str
    display_name: Optional[str] = None


class StorageCreate(BaseModel):
    name: str #TODO: enforce uniqueness


class StorageUpdate(BaseModel):
    name: str
    new_name: Optional[str] = None
    # TODO: think about handling updating the contents of storage.


class StorageDelete(BaseModel):
    name: str