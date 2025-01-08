# Author: Jure
# Date created: 4.12.2024

from datetime import datetime, timezone
from pydantic import BaseModel, Field, PastDatetime, field_serializer
from typing import Optional, List
import secrets

class Item(BaseModel):
    # TODO: This is a hack. This value should be provided by the Codes-MS microservice.
    # This is the unique identifier of the item.
    code_gen_token: str = Field(default=secrets.token_hex(16) )
    name: str
    amount: Optional[int] = Field(default=1)
    description: Optional[str] = Field(default=None)
    date_added: datetime = Field(default_factory=lambda data : datetime.now(tz=timezone.utc))
