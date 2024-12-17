# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .item import Item
from .py_object_id import PyObjectId


class Storage(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=PyObjectId)
    user_id: PyObjectId
    name: str
    content: List[Item]

    @field_serializer("id")
    def serialize_objectid(self, value: PyObjectId) -> str:
        return str(value)