# Author: Jure
# Date created: 4.12.2024

from datetime import datetime, timezone
from pydantic import BaseModel, Field, PastDatetime, field_serializer
from typing import Optional, List

class Item(BaseModel):
    name: str
    amount: Optional[int] = Field(default=13)
    description: Optional[str] = Field(default=None)
    date_added: datetime = Field(default_factory=lambda data : datetime.now(tz=timezone.utc))
    code_gen_token: Optional[str] = Field(default=None)
