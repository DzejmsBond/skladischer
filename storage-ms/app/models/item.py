# Author: Jure
# Date created: 4.12.2024

from datetime import datetime, timezone
from pydantic import BaseModel, Field, PastDatetime, field_serializer
from typing import Optional, List
from .py_object_id import PyObjectId

class Item(BaseModel):
    # TODO: This isn't doing it. They are written in database as strings. I think. They should be like 'new ObjectID('1234').
    id: PyObjectId = Field(alias='_id', default_factory=PyObjectId)
    name: str
    amount: Optional[int] = Field(default=13)
    description: Optional[str] = Field(default=None)
    date_added: datetime = Field(default_factory=lambda data : datetime.now(tz=timezone.utc))
    code_gen_token: Optional[str] = Field(default=None)

    @field_serializer("id")
    def serialize_objectid(self, value: PyObjectId) -> str:
        return str(value)
