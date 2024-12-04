# Author: Jure
# Date created: 4.12.2024

from datetime import datetime, timezone
from pydantic import BaseModel, Field, PastDatetime
from bson import ObjectId
from typing import Optional, List

class Item(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId)
    name: str
    amount: int = Field(default=1)
    description: Optional[str] = Field(default=None)
    date_added: datetime = Field(default_factory=datetime.now)  #TODO: Handle timezone later.
    code_gen_token: Optional[str] = Field(default=None)

