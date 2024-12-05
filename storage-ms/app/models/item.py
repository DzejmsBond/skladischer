# Author: Jure
# Date created: 4.12.2024

from datetime import datetime, timezone
from pydantic import BaseModel, Field, PastDatetime
from typing import Optional, List
from .objectIdWrapper import *

class Item(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    name: str
    amount: int = Field(default=1)
    description: Optional[str] = Field(default=None)
    date_added: datetime = Field(default_factory=datetime.now)  #TODO: Handle timezone later.
    code_gen_token: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    def set_id(self, oid : ObjectId):
        self.id = oid_to_str(oid)