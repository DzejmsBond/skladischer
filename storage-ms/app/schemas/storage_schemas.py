# Author: Nina Mislej
# Date created: 07.01.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional

class StorageCreate(BaseModel):
    name: str #TODO: enforce uniqueness.

class StorageUpdate(BaseModel):
    name: str
    new_name: Optional[str] = None
    # TODO: think about handling updating the contents of storage.

class ItemCreate(BaseModel):
    name: str
    amount: Optional[int]
    description: Optional[str]