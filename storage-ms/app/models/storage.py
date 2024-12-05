# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field
from typing import Optional, List
from .item import Item
from .objectIdWrapper import *

class Storage(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    name: str
    content: List[Item]

    class Config:
        arbitrary_types_allowed = True

    def set_id(self, oid : ObjectId):
        self.id = oid_to_str(oid)