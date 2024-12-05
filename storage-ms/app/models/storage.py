# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
from .item import Item

class Storage(BaseModel):
    id: int = 0 #Optional[ObjectId] = Field(default_factory=ObjectId)
    name: str
    content: List[Item]

    class Config:
        arbitrary_types_allowed = True